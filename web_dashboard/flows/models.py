import uuid
from uuid import uuid4
from datetime import datetime
from django.db import models


class OrgAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
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
class DataStore:
    id:uuid
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    owner: str
    type: str # postgres, kafka
    backend: str # airbyte-source, airbyte-destination
    backend_config:dict


class DataFlowInbound:
    id:uuid
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    owner: str
    source_store: DataStore
    destination_store: DataStore
    topic: str
    backend: str # airbyte-connection
    backend_config:dict


class DataView:
    id:uuid
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    owner: str
    data_flows: list[DataFlowInbound]
    query: str


class MLJob:
    id:uuid
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    owner: str
    view: DataView
    topic: str
    algorithm: str
    backend: str # batch, stream
    backend_config:dict


class DataFlowOutbound:
    id:uuid
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    owner: str
    source_topic: str
    destination_store: DataStore
    backend: str # airbyte-connection
    backend_config:dict


class Pipeline:
    id:uuid
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    owner: str
    inbound_flows: list[DataFlowInbound]
    views: list[DataView]
    ml_jobs: list[MLJob]
    outbound_flows: list[DataFlowOutbound]


class Workspace:
    id: uuid
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    owner: str
    data_stores: list[DataStore]
    data_flows: list[DataFlowInbound]
    data_views: list[DataView]
    ml_jobs: list[MLJob]
    outbound_flows: list[DataFlowOutbound]
    pipelines: list[Pipeline]

'''