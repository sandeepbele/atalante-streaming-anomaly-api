import json
import os

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, JsonResponse
from django.forms import ModelForm, modelform_factory
from django.views.decorators.http import require_POST
from .models import PostgresSource, PostgresSourceModel, SourceConfigurationModel
from .forms import JSONSchemaForm, JSONSchemaForm2, PostgresSourceForm, SourceFormFactory
from .airbyte_helper import AirbyteHelper
from django.shortcuts import reverse, redirect
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from .forms import JSONSchemaForm

from kafka import KafkaConsumer
import uuid
from .models import DataStore

airbyte_config = {
    "username": os.environ.get("AIRBYTE_USERNAME", "airbyte"),
    "password": os.environ.get("AIRBYTE_PASSWORD", ""),
    "host": os.environ.get("AIRBYTE_HOST", "localhost"),
    "port": int(os.environ.get("AIRBYTE_PORT", "8000")),
    "workspace_id": os.environ.get("AIRBYTE_WORKSPACE_ID", ""),
    #"destination_id": "635e05f3-5409-4554-8096-8a832766a39c"
    "destination_def_id": os.environ.get("AIRBYTE_DESTINATION_DEF_ID", "")
}


def index(request):
    return render(request, 'index.html')
    #return HttpResponse("Hello, world. You're at the web_dashboard index.")


def my_view(request):
    form = JSONSchemaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            # do something with the valid form data
            pass
    context = {'form': form}
    return render(request, 'index.html', context)


def show_sources(request):
    airbyte_client = AirbyteHelper(f"http://{airbyte_config['host']}:{airbyte_config['port']}",
                                   airbyte_config['username'],airbyte_config['password'])
    source_defs = airbyte_client.get_source_definitions(airbyte_config['workspace_id'])
    context = {'source_defs': source_defs}
    return render(request, 'sources.html', context=context)


@require_POST
def configure_source(request):

    form = None
    error = ""

    wizard_step = request.POST.get('wizard_step')
    if wizard_step is None:
        return redirect(reverse('show_sources'))

    source = request.POST.get('type')
    def_id = request.POST.get('def_id')

    if source is None or def_id is None:
        return redirect(reverse('show_sources'),context={'error':"select valid source."})

    if wizard_step == "show-form":
        if source == 'source-postgres':
            form = PostgresSourceForm()
            form.fields['type'].initial = source
            form.fields['def_id'].initial = def_id

            airbyte_client = AirbyteHelper(f"http://{airbyte_config['host']}:{airbyte_config['port']}",
                                           airbyte_config['username'], airbyte_config['password'])
            spec_json = airbyte_client.get_source_specification(airbyte_config['workspace_id'],
                                                                def_id)
            print("--spec_json--", json.dumps(spec_json, indent=2))

            print("--form--",form)

    elif wizard_step == "test-connection":
        if source == 'source-postgres':
            form = PostgresSourceForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data)
                print(form.get_source_config())

                source_id = None

                airbyte_client = AirbyteHelper(f"http://{airbyte_config['host']}:{airbyte_config['port']}",
                                               airbyte_config['username'], airbyte_config['password'])

                existing_instances = airbyte_client.search_source_instance_by_name(airbyte_config['workspace_id'],def_id,form.getName())

                if existing_instances:
                    for instance in existing_instances:
                        instance['connectionConfiguration'] == form.get_source_config()
                        source_id = instance['sourceId']
                        break

                if source_id is None:
                    status,error = airbyte_client.test_source_connection(airbyte_config['workspace_id'],def_id,form.get_source_config())

                    if status:
                        source_config = {
                                            "workspaceId": airbyte_config['workspace_id'],
                                            "sourceDefinitionId": def_id,
                                            "connectionConfiguration": form.get_source_config(),
                                            "name": form.getName()
                                          }

                        status_code, resp_json = airbyte_client.create_sources(source_config)
                        if status_code == 200:
                            source_id = resp_json['sourceId']

                            store = DataStore()
                            store.source_id = source_id
                            store.name = form.getName()
                            store.type = source
                            store.backend = 'airbyte-source'
                            store.backend_config = json.dumps(source_config)
                            store.save()

                        else:
                                error = f"creating source failed for {form.getName()}-{def_id}"

                if source_id:
                    return redirect(show_schema, source_id = source_id)

    if form is None:
        return redirect(reverse('show_sources'), context={'error': "select valid source."})

    context = {'form': form, 'errors': [ error ] if error else [] }
    return render(request, 'configure_source.html', context=context )


def show_schema(request, source_id):

    airbyte_client = AirbyteHelper(f"http://{airbyte_config['host']}:{airbyte_config['port']}",
                                   airbyte_config['username'], airbyte_config['password'])

    schema_status_code, schema_resp_json = airbyte_client.discover_source_schema(source_id)

    # fyi: schema_response_json = {'catalog': {'streams': [{'stream': {'name': 'anomalies', 'jsonSchema': {'type': 'object', 'properties....

    if schema_status_code == 200 and schema_resp_json['jobInfo']['succeeded'] == True:
        streams  = [ s['stream'] for s in schema_resp_json['catalog']['streams']]

        context = { 'source_id': source_id,
                    'stream_objects' : [ { 'name': stream['name'], 'schema': stream['jsonSchema'], 'cursor_field_options': list(stream['jsonSchema']['properties'].keys()) } for stream in streams]}

        return render(request, 'show_schema.html', context=context)


@require_POST
def show_schedule(request):

    source_id = request.POST.get('source_id')
    stream_name = request.POST.get('stream_name')
    cursor_field = request.POST.get('cursor_field')

    context = {'source_id': source_id,
               'stream_name': stream_name,
               'cursor_field': cursor_field,
              }

    return render(request, 'show_schedule.html', context=context)


def setup_sync(request):

    source_id = request.POST.get('source_id')
    stream_name = request.POST.get('stream_name')
    cursor_field = request.POST.get('cursor_field')
    schedule = request.POST.get('schedule')

    airbyte_client = AirbyteHelper(f"http://{airbyte_config['host']}:{airbyte_config['port']}",
                                   airbyte_config['username'], airbyte_config['password'])

    schema_status_code, schema_resp_json = airbyte_client.discover_source_schema(source_id)

    # fyi: schema_response_json = {'catalog': {'streams': [{'stream': {'name': 'anomalies', 'jsonSchema': {'type': 'object', 'properties....

    if schema_status_code == 200 and schema_resp_json['jobInfo']['succeeded'] == True:

        selected_stream_schema = [s['stream'] for s in schema_resp_json['catalog']['streams'] if s['stream']['name'] == stream_name][0]

        # create airbyte destination if it does not exist
        dest_search_req = {
            "destinationDefinitionId": airbyte_config['destination_def_id'],
            "workspaceId": airbyte_config['workspace_id']
        }
        dests = airbyte_client.search_dest_by_definition(airbyte_config['workspace_id'], airbyte_config['destination_def_id'])
        dest_id = None
        if len(dests) > 0:
            dest_id = dests[0]['destinationId']

        if dest_id is None:
            dest_create_req = {
                "name": "Kafka",
                "destinationDefinitionId": airbyte_config['destination_def_id'],
                "workspaceId": airbyte_config['workspace_id'],
                "connectionConfiguration": {
                    "socket_connection_setup_timeout_max_ms": "1",
                    "max_in_flight_requests_per_connection": 1,
                    "socket_connection_setup_timeout_ms": "1",
                    "receive_buffer_bytes": 1024,
                    "delivery_timeout_ms": 1,
                    "request_timeout_ms": 1,
                    "enable_idempotence": False,
                    "send_buffer_bytes": 1024,
                    "client_dns_lookup": "use_all_dns_ips",
                    "bootstrap_servers": "localhost:9092",
                    "max_request_size": 1024,
                    "compression_type": "none",
                    "topic_pattern": "{stream}",
                    "sync_producer": False,
                    "buffer_memory": "1024",
                    "max_block_ms": "1",
                    "batch_size": 3,
                    "linger_ms": "1",
                    "protocol": {"security_protocol": "PLAINTEXT"},
                    "retries": -26,
                    "acks": "1"
                }

            }

            dest_create_status, dest_create_resp = airbyte_client.create_destinations(dest_create_req)
            if dest_create_status == 200:
                dest_id = dest_create_resp['destinationId']
            else:
                return HttpResponseServerError("Could not create destination")

        ## we should have dest_id by this time or return error
        connection_request = {
            'sourceId': source_id,
            'destinationId': dest_id,
            "syncCatalog": {
                "streams": [
                    {
                        "config": {
                            "syncMode": "incremental",
                            "cursorField": [
                                cursor_field
                            ],
                            "destinationSyncMode": "append",
                            "primaryKey": [],
                            "aliasName": stream_name,
                            "selected": True,
                            "suggested": True
                        },
                        "stream": selected_stream_schema
                    }
                ]
            },
            "prefix": "",
            "namespaceDefinition": "destination",
            "namespaceFormat": "${SOURCE_NAMESPACE}",
            "nonBreakingChangesPreference": "ignore",
            "scheduleType": "basic",
            "scheduleData": {
                "basicSchedule": {
                    "units": 24,
                    "timeUnit": "hours"
                }
            },
            "geography": "auto",
            "name": "Postgres <> Kafka",
            "operations": [],
            "status": "active",
            "sourceCatalogId": schema_resp_json['catalogId']
        }

        print(connection_request)

        conn_status_code, conn_resp_json = airbyte_client.create_connection(connection_request)
        if conn_status_code == 200:
            connection_id = conn_resp_json['connectionId']
            name = conn_resp_json['name']
            topic = stream_name
            #sync_status_code, sync_resp_json = airbyte_client.trigger_connection_sync(connection_id)

            #if sync_status_code == 200:
            return render(request, 'sync_status.html',
                              context={'source_id': source_id,
                                       'connection_id': connection_id,
                                       'connection_name': name,
                                        'topic': topic,
                                       })
            #else:
            #    return HttpResponseServerError("sync failed")
        else:
            return HttpResponseServerError("connection failed")
    else:
        return HttpResponseServerError("schema discovery failed")

    return HttpResponseServerError("setting up source failed")


def sync_status(request):
    source_id = ""
    connection_id = ""
    name = "Postgres <> Kafka"
    topic = "ts_metrics"
    consumer_group = 'web_' + uuid.uuid4().hex
    return render(request, 'show_data_status.html',
                  context={'source_id': source_id,
                           'connection_id': connection_id,
                           'connection_name': name,
                           'topic': topic,
                           'consumer_group': consumer_group,
                           })


async def tailf_kafka(request,topic_name, consumer_group):

    messages = []

    c = KafkaConsumer(topic_name,
                      bootstrap_servers='localhost:9092',
                      auto_offset_reset='earliest',
                      group_id = consumer_group,
                      value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    index = 0
    for msg in c:
        messages.append(msg.value['_airbyte_data'])
        index += 1
        if index > 10:
            break

    c.close()

    return HttpResponse(json.dumps(messages), content_type="application/json")


def select_ml_process(request):
    wizard_step = request.POST.get('wizard_step')
    if wizard_step is None:
        return HttpResponseServerError("wizard step not found")

    if wizard_step == 'configure_ml':

        ml_tools = [
            { 'name': 'Anomaly Detection Using Half Space Trees', 'id': 'half_space_tree',
              'isEnabled': True,},
            { 'name': 'Anomaly Detection Using One Class SVM', 'id': 'one_class_svm','isEnabled': True,},
            { 'name': 'Anomaly Detection Using Gaussian Scorer', 'id': 'gaussian_scorer','isEnabled': True,},
            { 'name': 'Anomaly Detection Using Isolation Forest', 'id': 'isolation_forest','isEnabled': True,},
            { 'classification': 'Classification Using Logistic Regression','id': 'logistic_regression','isEnabled': True,},
        ]

        context = { 'connection_id': request.POST.get('connection_id'),
                    'topic': request.POST.get('topic'),
                    'connection_name': request.POST.get('connection_name'),
                    'consumer_group': request.POST.get('consumer_group'),
                    'wizard_step': wizard_step,
                    'ml_tools': ml_tools, }

        return render(request, 'ml_options.html', context=context)

    elif wizard_step == 'next_set_dest':

        pass


def select_destination(request):
    # find airbyte destination that matches id and return it
    # if not found, create one

    # create airbyte helper client
    airbyte_client = AirbyteHelper(f"http://{airbyte_config['host']}:{airbyte_config['port']}",
                                   airbyte_config['username'], airbyte_config['password'])

    # get all destinations
    destinations = airbyte_client.list_destinations(workspace_id=airbyte_config['workspace_id'])

    # find destination that matches id
    destination = None
    for dest in destinations:
        if dest['destinationDefinitionId'] == '25c5221d-dce2-4163-ade9-739ef790f503':
            destination = dest
            break

    context = {'destination': destination,
               'form': PostgresSourceForm(),}

    return render(request, 'select_destination.html', context=context)


def view_pipeline(request):
    return render(request, 'view_pipeline.html')

@csrf_exempt
def test_table_form(request):
    print(request.POST)
    return render(request, 'test_table_form.html')

@csrf_exempt
def fp_validate(request):
    print("--- fingerprint ---")
    #req = request.POST or request.GET or request.body or {}
    req = request.body.decode('utf-8')
    json.dump
    req_data = json.loads(req)
    fp_summary = dict()
    fp_summary['fp'] = req_data['fingerprint']
    print(json.dumps(req_data['fingerprint'].keys,indent=4,sort_keys=True))

    # return django json response with data
    return HttpResponse(json.dumps(json.loads(req)), content_type="application/json")


'''
uire_POST
def configure_source2(request):

    configured_source = 'none'
    form = None

    selected_source = request.POST.get('source_type')
    source_def_id = request.POST.get('source_def_id')

    if selected_source is not None:
        if selected_source == 'source-postgres':
            form = PostgresSourceForm()
            print("--form--",form)
        #form = SourceFormFactory.get_form(selected_source,
        #                                  source_id=selected_source,
        #                                  source_def_id=request.POST.get('source_def_id'))

        form = SourceFormFactory.get_form(selected_source, initial= { 'source_def_id': request.POST.get('source_def_id'),
                                            'source_type': selected_source})
        airbyte_client = AirbyteHelper(f"http://{airbyte_config['host']}:{airbyte_config['port']}",
                                       airbyte_config['username'], airbyte_config['password'])
        spec_json = airbyte_client.get_source_specification(airbyte_config['workspace_id'],request.POST.get('source_def_id'))
        print("--spec_json--",json.dumps(spec_json,indent=2))
        form = JSONSchemaForm2(spec_json, selected_source, source_def_id)
        print("--form--",form.as_p())

    else:
        configured_source = request.POST.get('configured_source')
        if configured_source is not None:
            if configured_source == 'source-postgres':
                form = JSONSchemaForm2(None,None,None,request.POST)

                if form.is_valid():
                    # do something with the valid form data
                    database = form.cleaned_data['host']
                    password = form.cleaned_data['password']
                    print("--database--",database)

                    # get list of existing sources in airbyte
                    # if source does not exist, create it
                    # if source exists, throw error
                    conn = AirbyteHelper("http://localhost:8000", "airbyte", os.environ.get("AIRBYTE_PASSWORD", ""))
                    return HttpResponseRedirect('/sources')

    context = {'configured_source': configured_source, 'form':form}
    return render(request, 'configure_source.html',context=context)
'''
