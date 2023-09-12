import random
import unittest
from typing import List

from airbyte import AirbyteEngine, AirbyteSourceInstance, AirbyteException, AirbyteSourceCatalog, AirbyteSourceStream, \
    AirbyteDestinationDefinition, AirbyteDestinationInstance, AirbyteConnection, SyncMode, Schedule
import json
from json import JSONEncoder


class CustomJsonEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


# Create your tests here.
class DataflowTests(unittest.TestCase):

    airbyte_config = {
        #"username": "airbyte",
        #"password": "password",
        #"host": "localhost",
        #"port": 8000,
        #"workspace_id": "5673a1b7-7d5a-453d-9311-243df1902581",
        #"destination_id": "635e05f3-5409-4554-8096-8a832766a39c"
        "destination_def_id": "9f760101-60ae-462f-9ee6-b7a9dafd454d",
        "airbyte_base_url": "http://localhost:8000",
        "client_id": "airbyte",
        "client_secret": "password",
        "workspace_id": "5673a1b7-7d5a-453d-9311-243df1902581",
    }

    def setUp(self):
        self.engine = AirbyteEngine(**self.airbyte_config)

    def test_def_loading(self):
        assert self.engine.get_source_def("decd338e-5647-4c0b-adf4-da0e75f5a750") is not None
        assert self.engine.get_source_def("d917a47b-8537-4d0d-8c10-36a9928d4265") is not None

    def test_postgres_source_def(self):
        src_def = self.engine.get_source_def("decd338e-5647-4c0b-adf4-da0e75f5a750")
        assert src_def is not None
        self.assertEqual(src_def.id, "decd338e-5647-4c0b-adf4-da0e75f5a750")
        self.assertEqual(src_def.name, "Postgres")
        assert src_def.icon is not None
        self.assertEqual(src_def.type, "source-postgres")
        self.assertEqual(src_def.isEnabled, True)

    def test_postgres_source_schema(self):
        src_def = self.engine.get_source_def("decd338e-5647-4c0b-adf4-da0e75f5a750")
        assert src_def is not None
        schema = self.engine.get_source_input_schema(src_def.id)
        assert schema is not None
        assert schema['properties'] is not None
        print(json.dumps(schema, indent=2))

    def test_create_postgres_source_instance(self):
        src_def = self.engine.get_source_def("decd338e-5647-4c0b-adf4-da0e75f5a750")
        assert src_def is not None
        source_config =  {  "replication_method": {"method": "Standard"},
                            "tunnel_method": {"tunnel_method": "NO_TUNNEL"}, "username": "postgres",
                            "ssl_mode": {"mode": "disable"}, "password": "mysecretpassword",
                            "database": "demo", "schemas": ["public"], "port": 5432, "host": "localhost",
                            "ssl": False
                          }
        src_instance = self.engine.create_source_instance("test-postgres-instance",src_def, source_config, test_connection=False)
        assert src_instance is not None
        self.assertIsInstance(src_instance, AirbyteSourceInstance)
        self.assertIsNotNone(src_instance.id)
        self.assertEqual(src_instance.name, "test-postgres-instance")
        self.assertEqual(src_instance.definition_id, src_def.id)
        self.assertEqual(src_instance.definition.name, src_def.name)
        print(json.dumps(src_instance, indent=2, cls=CustomJsonEncoder))

    def test_list_source_instance(self):
        src_instances = self.engine.list_source_instances()
        assert src_instances is not None
        self.assertGreater(len(src_instances), 0)
        print(json.dumps(src_instances, indent=2, cls=CustomJsonEncoder))

    def test_search_source_instance_by_name(self):
        src_instances = self.engine.search_source_instances(instance_name="test-postgres-instance")
        assert src_instances is not None
        self.assertGreater(len(src_instances), 0)
        print(json.dumps(src_instances, indent=2, cls=CustomJsonEncoder))

    def test_search_source_instance_by_def_id(self):
        src_instances = self.engine.search_source_instances(src_def="decd338e-5647-4c0b-adf4-da0e75f5a750")
        assert src_instances is not None
        self.assertGreater(len(src_instances), 0)
        print(json.dumps(src_instances, indent=2, cls=CustomJsonEncoder))

    def test_search_source_instance_by_def(self):
        src_def = self.engine.get_source_def("decd338e-5647-4c0b-adf4-da0e75f5a750")
        src_instances = self.engine.search_source_instances(src_def=src_def)
        assert src_instances is not None
        self.assertGreater(len(src_instances), 0)
        print(json.dumps(src_instances, indent=2, cls=CustomJsonEncoder))

    def test_source_connection_success(self):
        src_def = self.engine.get_source_def("decd338e-5647-4c0b-adf4-da0e75f5a750")
        assert src_def is not None
        source_config = {"replication_method": {"method": "Standard"},
                         "tunnel_method": {"tunnel_method": "NO_TUNNEL"}, "username": "postgres",
                         "ssl_mode": {"mode": "disable"}, "password": "mysecretpassword",
                         "database": "demo", "schemas": ["public"], "port": 5432, "host": "localhost",
                         "ssl": False
                         }
        status, error = self.engine.test_source_connection(src_def,source_config)
        self.assertTrue(status)

    def test_source_connection_failure(self):
        src_def = self.engine.get_source_def("decd338e-5647-4c0b-adf4-da0e75f5a750")
        assert src_def is not None
        wrong_source_config = {"replication_method": {"method": "Standard"},
                         "tunnel_method": {"tunnel_method": "NO_TUNNEL"}, "username": "postgres",
                         "ssl_mode": {"mode": "disable"}, "password": "WRONGPASSWORD",
                         "database": "demo", "schemas": ["public"], "port": 5432, "host": "localhost",
                         "ssl": False
                         }
        status, error = self.engine.test_source_connection(src_def,wrong_source_config)
        self.assertFalse(status)

    def test_create_postgres_source_instance_with_test_connection_success(self):
        src_def = self.engine.get_source_def("decd338e-5647-4c0b-adf4-da0e75f5a750")
        assert src_def is not None
        source_config =  {  "replication_method": {"method": "Standard"},
                            "tunnel_method": {"tunnel_method": "NO_TUNNEL"}, "username": "postgres",
                            "ssl_mode": {"mode": "disable"}, "password": "mysecretpassword",
                            "database": "demo", "schemas": ["public"], "port": 5432, "host": "localhost",
                            "ssl": False
                          }
        src_instance = self.engine.create_source_instance("test-postgres-instance",src_def, source_config, test_connection=True)
        assert src_instance is not None
        self.assertIsInstance(src_instance, AirbyteSourceInstance)
        self.assertIsNotNone(src_instance.id)
        self.assertEqual(src_instance.name, "test-postgres-instance")
        self.assertEqual(src_instance.definition_id, src_def.id)
        self.assertEqual(src_instance.definition.name, src_def.name)
        print(json.dumps(src_instance, indent=2, cls=CustomJsonEncoder))

    def test_create_postgres_source_instance_with_test_connection_failure(self):
        src_def = self.engine.get_source_def("decd338e-5647-4c0b-adf4-da0e75f5a750")
        assert src_def is not None
        source_config = {"replication_method": {"method": "Standard"},
                         "tunnel_method": {"tunnel_method": "NO_TUNNEL"}, "username": "postgres",
                         "ssl_mode": {"mode": "disable"}, "password": "WRONG_PASSWORD",
                         "database": "demo", "schemas": ["public"], "port": 5432, "host": "localhost",
                         "ssl": False
                         }

        with self.assertRaises(AirbyteException) as ex:
            self.engine.create_source_instance("test-postgres-instance", src_def, source_config,
                                                          test_connection=True)

    def test_discover_source_catalogue(self):
        src_def = self.engine.get_source_def("decd338e-5647-4c0b-adf4-da0e75f5a750")
        src_instances = self.engine.search_source_instances(src_def=src_def)
        self.assertGreater(len(src_instances), 0)
        src_inst = src_instances[0]

        catalogue = self.engine.discover_source_data_catalog(src_inst)
        self.assertIsInstance(catalogue,AirbyteSourceCatalog)
        print(json.dumps(catalogue, indent=2, cls=CustomJsonEncoder))

        self.assertGreater(len(catalogue.streams),0)
        #self.assertIsInstance(catalogue.streams, List[AirbyteSourceStream])
        stream = catalogue.streams[0]
        self.assertIsNotNone(stream.name)
        self.assertIsNotNone(stream.schema)
        self.assertGreater(len(stream.get_fields()),0)
        self.assertGreater(len(stream.get_datetime_fields()),0)
        self.assertIsNotNone(catalogue.id)

    def test_get_destination_def(self):
        dest_def = self.engine.get_destination_def("9f760101-60ae-462f-9ee6-b7a9dafd454d")
        self.assertIsNotNone(dest_def)
        self.assertIsInstance(dest_def, AirbyteDestinationDefinition)
        print(json.dumps(dest_def, indent=2, cls=CustomJsonEncoder))

    def test_get_destination_input_schema(self):
        dest_def = self.engine.get_destination_def("9f760101-60ae-462f-9ee6-b7a9dafd454d")
        self.assertIsNotNone(dest_def)
        self.assertIsInstance(dest_def, AirbyteDestinationDefinition)
        #print(json.dumps(dest_def, indent=2, cls=CustomJsonEncoder))
        input_schema = self.engine.get_destination_input_schema(dest_def)
        self.assertIsNotNone(input_schema)
        print(json.dumps(input_schema, indent=2, cls=CustomJsonEncoder))

    def test_create_destination_instance(self):
        dest_def = self.engine.get_destination_def("9f760101-60ae-462f-9ee6-b7a9dafd454d")
        self.assertIsNotNone(dest_def)
        self.assertIsInstance(dest_def, AirbyteDestinationDefinition)
        #print(json.dumps(dest_def, indent=2, cls=CustomJsonEncoder))
        input_schema = self.engine.get_destination_input_schema(dest_def)
        #self.assertIsNotNone(input_schema)
        #print(json.dumps(input_schema, indent=2, cls=CustomJsonEncoder))
        dest_config = {
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
        dest_instance = self.engine.create_destination_instance("test-destination-kafka-instance", dest_def, dest_config)
        self.assertIsNotNone(dest_instance)
        self.assertIsInstance(dest_instance, AirbyteDestinationInstance)
        self.assertIsNotNone(dest_instance.destination_id)
        self.assertEqual(dest_instance.definition_id, dest_def.id)
        self.assertEqual(dest_instance.name, "test-destination-kafka-instance")
        print(json.dumps(dest_instance, indent=2, cls=CustomJsonEncoder))

    def test_destination_connection_success(self):
        dest_def = self.engine.get_destination_def("9f760101-60ae-462f-9ee6-b7a9dafd454d")
        self.assertIsNotNone(dest_def)
        self.assertIsInstance(dest_def, AirbyteDestinationDefinition)
        #print(json.dumps(dest_def, indent=2, cls=CustomJsonEncoder))
        config = dest_config = {
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

        status,error = self.engine.test_destination_connection(dest_def, config)
        self.assertTrue(status)

    def test_list_destination_instances(self):
        dest_instances = self.engine.list_destination_instances()
        self.assertIsNotNone(dest_instances)
        self.assertGreater(len(dest_instances), 0)
        print(json.dumps(dest_instances, indent=2, cls=CustomJsonEncoder))

    def test_search_destination_instances_by_name(self):
        dest_instances = self.engine.search_destination_instances(instance_name="test-destination-kafka-instance")
        self.assertIsNotNone(dest_instances)
        self.assertGreater(len(dest_instances), 0)
        print(json.dumps(dest_instances, indent=2, cls=CustomJsonEncoder))

    def test_search_destination_instance_by_def(self):
        dest_instances = self.engine.search_destination_instances(dest_def_id="9f760101-60ae-462f-9ee6-b7a9dafd454d")
        self.assertIsNotNone(dest_instances)
        self.assertGreater(len(dest_instances), 0)
        print(json.dumps(dest_instances, indent=2, cls=CustomJsonEncoder))

    def test_source_instance_equality_by_config(self):

        src_def = self.engine.get_source_def("decd338e-5647-4c0b-adf4-da0e75f5a750")
        assert src_def is not None
        source_config = {"replication_method": {"method": "Standard"},
                         "tunnel_method": {"tunnel_method": "NO_TUNNEL"}, "username": "postgres",
                         "ssl_mode": {"mode": "disable"}, "password": "mysecretpassword",
                         "database": "demo", "schemas": ["public"], "port": 5432, "host": "localhost",
                         "ssl": False
                         }

        instance_one = AirbyteSourceInstance({ "name": "test-source-postgres-instance",
                         "sourceDefinitionId": "decd338e-5647-4c0b-adf4-da0e75f5a750",
                         "workspaceId": "1",
                         "connectionConfiguration": source_config
                        }, src_def)

        # change order of config by sorting
        instance_two = AirbyteSourceInstance({ "name": "test-source-postgres-instance-2",
                            "sourceDefinitionId": "decd338e-5647-4c0b-adf4-da0e75f5a750",
                            "workspaceId": "1",
                            "connectionConfiguration": dict(sorted(source_config.items()))
                         }, src_def)

        self.assertTrue(instance_one.has_same_config(instance_two))

        # different property : port
        instance_three = AirbyteSourceInstance({ "name": "test-source-postgres-instance-3",
                                                 "sourceDefinitionId": "decd338e-5647-4c0b-adf4-da0e75f5a750",
                                                 "workspaceId": "1",
                                                 "connectionConfiguration": { **source_config, "port": 5433}
                                                 }, src_def)

        self.assertFalse(instance_one.has_same_config(instance_three))

    def test_get_or_create_source_instance(self):
        src_def = self.engine.get_source_def("decd338e-5647-4c0b-adf4-da0e75f5a750")
        assert src_def is not None
        source_config = {"replication_method": {"method": "Standard"},
                         "tunnel_method": {"tunnel_method": "NO_TUNNEL"}, "username": "postgres",
                         "ssl_mode": {"mode": "disable"}, "password": "mysecretpassword",
                         "database": "demo", "schemas": ["public"], "port": 5432, "host": "localhost",
                         "ssl": False
                         }
        instances_before = self.engine.search_source_instances(src_def=src_def)
        src_instance = self.engine.get_or_create_source_instance("test-postgres-instance", src_def, source_config,
                                                          test_connection=True)
        instances_after = self.engine.search_source_instances(src_def=src_def)
        self.assertIsNotNone(src_instance)

        # since we know instance with that name exist
        self.assertEqual(len(instances_after), len(instances_before))

        # create new instance with different name
        src_instance = self.engine.get_or_create_source_instance("test-postgres-instance_"+str(random.randint(1,100)), src_def, source_config,
                                                                 test_connection=True)
        instances_after = self.engine.search_source_instances(src_def=src_def)
        self.assertIsNotNone(src_instance)
        self.assertEqual(len(instances_after), len(instances_before)+1)

    def test_setup_connection(self):
        source_instances = self.engine.search_source_instances(instance_name="test-postgres-instance")
        self.assertIsNotNone(source_instances)
        dest_instances = self.engine.search_destination_instances(instance_name="test-destination-kafka-instance")
        self.assertIsNotNone(dest_instances)
        connection = self.engine.setup_connection( "test-connection",
                                                    source_instances[0],
                                                    dest_instances[0],
                                                    "ts_metrics",
                                                    "ts",
                                                    SyncMode.INCREMENTAL,
                                                    Schedule()
                                                   )

        self.assertIsNotNone(connection)
        self.assertIsInstance(connection, AirbyteConnection)
        self.assertIsNotNone(connection.id)
        self.assertEqual(connection.name, "test-connection")
        self.assertEqual(connection.source_id, source_instances[0].id)
        self.assertEqual(connection.destination_id, dest_instances[0].id)
        self.assertEqual(connection.stream.name, "ts_metrics")
        self.assertFalse(connection.is_active())

    def test_start_stop_connection(self):
        source_instances = self.engine.search_source_instances(instance_name="test-postgres-instance")
        self.assertIsNotNone(source_instances)
        dest_instances = self.engine.search_destination_instances(instance_name="test-destination-kafka-instance")
        self.assertIsNotNone(dest_instances)
        connection = self.engine.setup_connection("test-connection",
                                                  source_instances[0],
                                                  dest_instances[0],
                                                  "ts_metrics",
                                                  "ts",
                                                  SyncMode.INCREMENTAL,
                                                  Schedule()
                                                  )

        self.assertIsNotNone(connection)
        self.assertIsInstance(connection, AirbyteConnection)
        self.assertIsNotNone(connection.id)
        self.assertEqual(connection.name, "test-connection")
        self.assertEqual(connection.source_id, source_instances[0].id)
        self.assertEqual(connection.destination_id, dest_instances[0].id)
        self.assertEqual(connection.stream.name, "ts_metrics")
        self.assertFalse(connection.is_active())

        connection = self.engine.start_dataflow(connection)
        self.assertTrue(connection.is_active())

        connection = self.engine.stop_dataflow(connection)
        self.assertFalse(connection.is_active())


''' 
    def test_create_source(self):   
        pass

    def test_create_destination(self):
        pass

    def test_create_connection(self):
        pass

    def test_start_connection(self):
        pass

    def test_stop_connection(self):
        pass

    def test_get_source_def(self):
        pass

    def test_get_source_instance(self):
        pass

    def test_get_destination_def(self):
        pass

    def test_get_destination_instance(self):
        pass

    def test_get_connection(self):
        pass

    def teardown(self):
        pass
'''