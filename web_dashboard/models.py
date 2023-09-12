from abc import abstractmethod
from django.contrib.auth.models import User

from pydantic import BaseModel, Field
from django.db import models
from uuid import uuid4

ACC_TYPES = (('dev','developer'),('ent','enterprise'))


class OrgAccount(models.Model):

    class Meta:
        db_table = "anm_orgaccount"

    id = models.UUIDField(primary_key=True, default=uuid4)
    type = models.TextField(choices=ACC_TYPES)
    billing_plan = models.TextField(default='free')
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    type = models.TextField(null=True)  # dev, prod
    is_active = models.BooleanField(null=True, default=True)
    is_deleted = models.BooleanField(null=True, default=False)
    is_suspended = models.BooleanField(null=True, default=False)
    is_demo = models.BooleanField(null=True, default=False)
    is_trial = models.BooleanField(null=True, default=False)

    def __str__(self):
        return str(self.name)


class UserAccount(models.Model):

    class Meta:
        db_table = "anm_useraccount"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    org = models.ForeignKey(OrgAccount, on_delete=models.CASCADE)
    api_key = models.TextField(null=True)
    email_verified = models.BooleanField(null=True, default=False)
    email_verification_sent = models.BooleanField(null=True,default=False)
    email_verified_at = models.DateTimeField(null=True)
    welcome_email_sent = models.BooleanField(null=True,default=False)
    welcome_email_sent_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_admin = models.BooleanField(null=True, default=False)
    is_active = models.BooleanField(null=True, default=True)
    is_deleted = models.BooleanField(null=True, default=False)
    is_suspended = models.BooleanField(null=True, default=False)

    def __str__(self):
        return str(self.user.username+"#"+str(self.org.name))

'''
class OrgAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    owner = models.TextField(null=True)
    type = models.TextField(null=True) # dev, prod
    billing_plan = models.TextField(null=True) # free, paid
    is_active = models.BooleanField(null=True, default=True)
    is_deleted = models.BooleanField(null=True, default=False)
    is_suspended = models.BooleanField(null=True, default=False)
    is_demo = models.BooleanField(null=True, default=False)
    is_trial = models.BooleanField(null=True, default=False)


class UserAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    owner = models.TextField(null=True)
    api_key = models.TextField(null=True)
    email_verified = models.BooleanField(null=True, default=False)
    email_verification_sent = models.BooleanField(null=True,default=False)
    email_verified_at = models.DateTimeField(null=True)
    welcome_email_sent = models.BooleanField(null=True,default=False)
    welcome_email_sent_at = models.DateTimeField(null=True)
    org = models.ForeignKey(OrgAccount, on_delete=models.CASCADE)
    is_admin = models.BooleanField(null=True, default=False)
    is_active = models.BooleanField(null=True, default=True)
    is_deleted = models.BooleanField(null=True, default=False)
    is_suspended = models.BooleanField(null=True, default=False)

'''


class DataStore(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    type = models.TextField(null=True) # postgres, kafka
    backend = models.TextField(null=True) # airbyte-source, airbyte-destination
    backend_config = models.JSONField(null=True)


class DataFlow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    source_store = models.ForeignKey(DataStore, on_delete=models.CASCADE, related_name='source_store')
    destination_store = models.ForeignKey(DataStore, on_delete=models.CASCADE, related_name='destination_store')
    topic = models.TextField(null=True)
    backend = models.TextField(null=True) # airbyte-connection
    backend_config = models.JSONField(null=True)


class DataView(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    data_flows = models.ManyToManyField(DataFlow)
    query = models.TextField(null=True)


class MLJob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    data_view = models.ForeignKey(DataView, on_delete=models.CASCADE)
    backend = models.TextField(null=True) # batch, stream
    backend_config = models.JSONField(null=True)
    topic = models.TextField(null=True)


class Pipeline(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    inbound_flows = models.ManyToManyField(DataFlow, related_name='inbound_flows')
    views = models.ManyToManyField(DataView)
    ml_jobs = models.ManyToManyField(MLJob)
    outbound_flows = models.ManyToManyField(DataFlow, related_name='outbound_flows')


class Workspace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    data_stores = models.ManyToManyField(DataStore)
    data_flows = models.ManyToManyField(DataFlow)
    data_views = models.ManyToManyField(DataView)
    ml_jobs = models.ManyToManyField(MLJob)
    pipelines = models.ManyToManyField(Pipeline)


class PostgresSource(BaseModel):
    host: str = Field("localhost", description="The host of the postgres database")
    post: int = Field(5432, description="The port of the postgres database")
    schemas: list = Field(["public"], description="The schemas of the postgres database")
    database: str = Field("demo", description="The database of the postgres database")
    username: str = Field("postgres", description="The username of the postgres database")
    password: str = Field("password", description="The password of the postgres database")
    ssl: bool = Field(False, description="The ssl of the postgres database")
    ssl_mode: str = Field("disable", description="The ssl mode of the postgres database")
    tunnel_method: str = Field("NO_TUNNEL", description="The tunnel method of the postgres database")
    replication_method: str = Field("Standard", description="The replication method of the postgres database")


class SourceConfigurationModel(models.Model):
    type: str
    configuration: dict

    def get_config_model(self):

        if self.type == 'postgres':
            return PostgresSourceModel(**self.configuration)
        else:
            raise ValueError(f"Invalid config type: {type}")


class PostgresSourceModel(models.Model):

    class SSLChoices(models.TextChoices):
        DISABLE = "disable"
        ALLOW = "allow"
        PREFER = "prefer"
        REQUIRE = "require"
        VERIFY_CA = "verify-ca"
        VERIFY_FULL = "verify-full"

    class SSLTunnelChoices(models.TextChoices):
        NO_TUNNEL = "NO_TUNNEL"
        SSH_TUNNEL = "SSH_TUNNEL"
        SSH_TUNNEL_WITH_PASSWORD = "SSH_TUNNEL_WITH_PASSWORD"
        SSH_TUNNEL_WITH_KEY = "SSH_TUNNEL_WITH_KEY"
        SSH_TUNNEL_WITH_AGENT = "SSH_TUNNEL_WITH_AGENT"
        SSH_TUNNEL_WITH_PASSWORD_AND_KEY = "SSH_TUNNEL_WITH_PASSWORD_AND_KEY"

    class ReplicationMethodChoices(models.TextChoices):
        STANDARD = "Standard"
        LOGICAL = "Logical"


    host = models.TextField()
    port = models.IntegerField()
    schemas = models.TextField()
    database = models.TextField()
    username = models.TextField()
    password = models.TextField()
    ssl = models.BooleanField()
    ssl_mode = models.CharField(choices=SSLChoices.choices, max_length=20)
    tunnel_method = models.CharField(choices=SSLTunnelChoices.choices, max_length=40)
    replication_method = models.CharField(choices=ReplicationMethodChoices.choices, max_length=20)




class DataflowEngine:
    @abstractmethod
    def get_connection(self):
        pass


class AirbyteEngine(DataflowEngine):
    pass


class DataflowSource:
    pass


class AirbyteSource(DataflowSource):
    engine = AirbyteEngine()
    pass


class DataflowDestination:
    pass


class AirbyteDestination(DataflowDestination):
    engine = AirbyteEngine()
    pass


class DataflowConnection:

    source:DataflowSource
    destination:DataflowDestination
    inSchema = None
    outSchema = None

    def __int__(self, source, destination):
        self.source = source
        self.destination = destination
        pass

    def start(self):
        pass

    def stop(self):
        pass


class AirbyteConnection(DataflowConnection):
    engine = AirbyteEngine()



class MLProcessor:
    in_schema = None
    out_schema = None
    pass


class AnomalyDetector(MLProcessor):
    pass


class DmlPipe():
    in_flow:DataflowConnection = None
    ml_flow:MLProcessor = None
    out_flow:DataflowConnection = None
    in_topic = None
    out_topic = None

    def validate(self):
        if not self.in_flow.outSchema == self.ml_flow.in_schema:
            raise ValueError("Incompatible schemas")
        pass
    pass

'''
def test_all_nonsense():

    airbyte_engine = AirbyteEngine(**config)
    postgres_source_def = airbyte_engine.get_source_def(AirbyteEngine.SourceType.POSTGRES)
    postgres_source = airbyte_engine.get_source_instance(postgres_source_def, config)
    postgres_source = airbyte_engine.create_source(config)

    kafka_destination_def = airbyte_engine.get_destination_def(AirbyteEngine.DestinationType.KAFKA)
    kafka_destination = airbyte_engine.get_destination_instance(kafka_destination_def, config)
    kafka_destination = airbyte_engine.create_destination(config)

    postgres_to_kafka_connection = airbyte_engine.create_connection(postgres_source, kafka_destination)
    kafka_to_postgres_connection = airbyte_engine.create_connection(kafka_destination, postgres_source)
    ml_processor = AnomalyDetector()

    pipe = DmlPipe(postgres_to_kafka_connection, ml_processor, kafka_to_postgres_connection)

    pipe.validate()

    pipe.start()
    pipe.stop()

    pipe.get_status()
    pipe.get_logs()
    pipe.get_metrics()
'''