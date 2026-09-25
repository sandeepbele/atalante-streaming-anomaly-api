from django.test import TestCase
from app.models import OrgAccount, UserAccount, DataStore, DataFlow, DataView, MLJob, Pipeline


class utils:

    def create_org(name, type, billing_plan, **kwargs):
        org = OrgAccount(name=name,type=type,billing_plan=billing_plan)
        org.save()
        return org

    def create_user(name, org: OrgAccount):
        user = UserAccount(name=name, org=org)
        user.save()
        return user

    def create_datastore(name, owner:UserAccount, type,backend, backend_config):
        datastore = DataStore(name=name, owner=owner, type=type, backend=backend, backend_config=backend_config)
        datastore.save()
        return datastore

    def create_dataflow(name, owner:UserAccount, source_store:DataStore, destination_store:DataStore, topic, backend, backend_config):
        dataflow = DataFlow(name=name, owner=owner, source_store=source_store, destination_store=destination_store, topic=topic, backend=backend, backend_config=backend_config)
        dataflow.save()
        return dataflow


class DbModelTests(TestCase):

    def test_orgaccount(self):

        org = OrgAccount()
        org.name = "test"
        org.type = "dev"
        org.billing_plan = "free"
        org.save()
        self.assertEqual(org.name, "test")
        self.assertEqual(org.type, "dev")
        self.assertEqual(org.billing_plan, "free")
        self.assertTrue(org.is_active)
        self.assertFalse(org.is_deleted)
        self.assertFalse(org.is_suspended)
        self.assertFalse(org.is_demo)
        self.assertFalse(org.is_trial)
        self.assertIsNotNone(org.created_at)
        self.assertIsNotNone(org.updated_at)
        self.assertIsNotNone(org.id)
        org.delete()
        pass

    def test_useraccount(self):

        user = UserAccount()
        user.name = "test_user_1"
        user.org = OrgAccount()
        user.org.name = "test"
        user.org.type = "dev"
        user.org.billing_plan = "free"
        user.save()
        self.assertEqual(user.name, "test_user_1")
        self.assertEqual(user.org.name, "test")
        self.assertEqual(user.org.type, "dev")
        self.assertEqual(user.org.billing_plan, "free")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_deleted)
        self.assertFalse(user.is_suspended)
        self.assertFalse(user.is_admin)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
        self.assertIsNotNone(user.id)
        user.delete()

    def test_datastore(self):

        org = OrgAccount()
        org.name = "test"
        org.type = "dev"
        org.billing_plan = "free"
        org.save()

        user = UserAccount()
        user.name = "test_user_1"
        user.org = org
        user.save()

        datastore = DataStore()
        datastore.name = "test_datastore_1"
        datastore.owner = user
        datastore.type = "postgres"
        datastore.backend = "airbyte-source"
        datastore.backend_config= {"username":"test","password":"test","host":"test","port":"test","database":"test"}

        datastore.save()

        self.assertEqual(datastore.name, "test_datastore_1")
        self.assertEqual(datastore.owner.name, "test_user_1")
        self.assertEqual(datastore.owner.org.name, "test")
        self.assertEqual(datastore.owner.org.type, "dev")
        self.assertEqual(datastore.owner.org.billing_plan, "free")
        self.assertEqual(datastore.type, "postgres")
        self.assertEqual(datastore.backend, "airbyte-source")
        self.assertEqual(datastore.backend_config, {"username":"test","password":"test","host":"test","port":"test","database":"test"})
        self.assertIsNotNone(datastore.created_at)
        self.assertIsNotNone(datastore.updated_at)
        self.assertIsNotNone(datastore.id)

        datastore.delete()
        user.delete()
        org.delete()

    def test_dataflow(self):

        org = utils.create_org("test", "dev", "free")
        user = utils.create_user("test_user_1", org)
        datastore = utils.create_datastore("test_datastore_1", user, "postgres","airbyte-source", {"username":"test","password":"test","host":"test","port":"test","database":"test"})
        datastore2 = utils.create_datastore("test_datastore_2", user, "postgres","airbyte-source", {"username":"test","password":"test","host":"test","port":"test","database":"test"})

        dataflow = DataFlow()
        dataflow.name = "test_dataflow_1"
        dataflow.owner = user
        dataflow.source_store = datastore
        dataflow.destination_store = datastore2
        dataflow.topic = "test_topic"
        dataflow.save()

        self.assertEqual(dataflow.name, "test_dataflow_1")
        self.assertEqual(dataflow.owner.name, "test_user_1")
        self.assertEqual(dataflow.owner.org.name, "test")
        self.assertEqual(dataflow.owner.org.type, "dev")
        self.assertEqual(dataflow.owner.org.billing_plan, "free")
        self.assertEqual(dataflow.source_store.name, "test_datastore_1")
        self.assertEqual(dataflow.source_store.owner.name, "test_user_1")
        self.assertEqual(dataflow.source_store.owner.org.name, "test")
        self.assertEqual(dataflow.source_store.owner.org.type, "dev")
        self.assertEqual(dataflow.source_store.owner.org.billing_plan, "free")
        self.assertEqual(dataflow.destination_store.name, "test_datastore_2")
        self.assertEqual(dataflow.destination_store.owner.name, "test_user_1")
        self.assertEqual(dataflow.destination_store.owner.org.name, "test")
        self.assertEqual(dataflow.destination_store.owner.org.type, "dev")
        self.assertEqual(dataflow.destination_store.owner.org.billing_plan, "free")
        self.assertIsNotNone(dataflow.created_at)
        self.assertIsNotNone(dataflow.updated_at)
        self.assertEqual(dataflow.topic, "test_topic")
        self.assertIsNotNone(dataflow.id)

        dataflow.delete()

    def test_dataview(self):

        org = utils.create_org("test", "dev", "free")
        user = utils.create_user("test_user_1", org)

        datastore = utils.create_datastore("test_datastore_1", user, "postgres", "airbyte-source", {"username":"test","password":"test","host":"test","port":"test","database":"test"})
        dataflow = utils.create_dataflow("test_dataflow_1", user, datastore, datastore, "test_topic_1",None,None)
        dataflow2 = utils.create_dataflow("test_dataflow_2", user, datastore, datastore, "test_topic_2",None,None)

        dataview = DataView()
        dataview.name = "test_dataview_1"
        dataview.owner = user
        dataview.data_flows.add(dataflow, dataflow2)
        dataview.query = "select * from test"
        dataview.save()

        self.assertEqual(dataview.name, "test_dataview_1")
        self.assertEqual(dataview.owner.name, "test_user_1")
        self.assertEqual(dataview.owner.org.name, "test")
        self.assertEqual(dataview.owner.org.type, "dev")
        self.assertEqual(dataview.owner.org.billing_plan, "free")
        self.assertIsNotNone(dataview.created_at)
        self.assertIsNotNone(dataview.updated_at)
        self.assertIsNotNone(dataview.id)
        self.assertEqual(dataview.query, "select * from test")
        self.assertEqual(dataview.data_flows.all().order_by("name")[0].name, "test_dataflow_1")
        self.assertEqual(dataview.data_flows.all().order_by("name")[0].owner.name, "test_user_1")
        self.assertEqual(dataview.data_flows.all().order_by("name")[1].name, "test_dataflow_2")
        self.assertEqual(dataview.data_flows.all().order_by("name")[1].owner.name, "test_user_1")
        self.assertEqual(dataview.data_flows.all().order_by("name")[0].topic, "test_topic_1")
        self.assertEqual(dataview.data_flows.all().order_by("name")[1].topic, "test_topic_2")

        dataview.delete()

    def test_mljob(self):

        org = utils.create_org("test", "dev", "free")
        user = utils.create_user("test_user_1", org)
        datastore = utils.create_datastore("test_datastore_1", user, "postgres", "airbyte-source", {"username":"test","password":"test","host":"test","port":"test","database":"test"})
        dataflow = utils.create_dataflow("test_dataflow_1", user, datastore, datastore, "test_topic_1",None,None)
        dataflow2 = utils.create_dataflow("test_dataflow_2", user, datastore, datastore, "test_topic_2",None,None)

        dataview = DataView()
        dataview.name = "test_dataview_1"
        dataview.owner = user
        dataview.data_flows.add(dataflow, dataflow2)
        dataview.query = "select * from test"
        dataview.save()

        mljob = MLJob()
        mljob.name = "test_mljob_1"
        mljob.owner = user
        mljob.data_view = dataview
        mljob.backend = "stream"
        mljob.backend_config = {"stream_config":"dummy"}
        mljob.save()

        self.assertEqual(mljob.name, "test_mljob_1")
        self.assertEqual(mljob.owner.name, "test_user_1")
        self.assertEqual(mljob.owner.org.name, "test")
        self.assertEqual(mljob.owner.org.type, "dev")
        self.assertEqual(mljob.owner.org.billing_plan, "free")
        self.assertEqual(mljob.backend, "stream")
        self.assertEqual(mljob.backend_config, {"stream_config":"dummy"})
        self.assertIsNotNone(mljob.created_at)
        self.assertIsNotNone(mljob.updated_at)
        self.assertIsNotNone(mljob.id)
        self.assertEqual(mljob.data_view.name, "test_dataview_1")
        self.assertEqual(mljob.data_view.owner.name, "test_user_1")
        self.assertEqual(mljob.data_view.owner.org.name, "test")
        self.assertEqual(mljob.data_view.owner.org.type, "dev")
        self.assertEqual(mljob.data_view.owner.org.billing_plan, "free")
        self.assertEqual(mljob.data_view.query, "select * from test")

        mljob.delete()
        dataview.delete()
        dataflow.delete()
        dataflow2.delete()
        datastore.delete()
        user.delete()
        org.delete()

    def test_pipeline(self):

            org = utils.create_org("test", "dev", "free")
            user = utils.create_user("test_user_1", org)
            datastore = utils.create_datastore("test_datastore_1", user, "postgres", "airbyte-source", {"username":"test","password":"test","host":"test","port":"test","database":"test"})
            dataflow = utils.create_dataflow("test_dataflow_1", user, datastore, datastore, "test_topic_1",None,None)
            dataflow2 = utils.create_dataflow("test_dataflow_2", user, datastore, datastore, "test_topic_2",None,None)

            dataview = DataView()
            dataview.name = "test_dataview_1"
            dataview.owner = user
            dataview.data_flows.add(dataflow, dataflow2)
            dataview.query = "select * from test"
            dataview.save()

            mljob = MLJob()
            mljob.name = "test_mljob_1"
            mljob.owner = user
            mljob.data_view = dataview
            mljob.backend = "stream"
            mljob.backend_config = {"stream_config":"dummy"}
            mljob.save()

            pipeline = Pipeline()
            pipeline.name = "test_pipeline_1"
            pipeline.owner = user
            pipeline.ml_jobs.add(mljob)
            pipeline.views.add(dataview)
            pipeline.inbound_flows.add(dataflow)
            pipeline.outbound_flows.add(dataflow2)
            pipeline.save()

            self.assertEqual(pipeline.name, "test_pipeline_1")
            self.assertEqual(pipeline.owner.name, "test_user_1")
            self.assertEqual(pipeline.owner.org.name, "test")
            self.assertEqual(pipeline.owner.org.type, "dev")
            self.assertEqual(pipeline.owner.org.billing_plan, "free")
            self.assertIsNotNone(pipeline.created_at)
            self.assertIsNotNone(pipeline.updated_at)
            self.assertIsNotNone(pipeline.id)
            self.assertEqual(pipeline.views.all().order_by("name")[0].name, "test_dataview_1")
            self.assertEqual(pipeline.views.all().order_by("name")[0].owner.name, "test_user_1")
            self.assertEqual(pipeline.inbound_flows.all().order_by("name")[0].name, "test_dataflow_1")
            self.assertEqual(pipeline.outbound_flows.all().order_by("name")[0].name, "test_dataflow_2")
            self.assertEqual(pipeline.ml_jobs.all().order_by("name")[0].name, "test_mljob_1")
            self.assertEqual(pipeline.ml_jobs.all().order_by("name")[0].owner.name, "test_user_1")
            self.assertEqual(pipeline.ml_jobs.all().order_by("name")[0].owner.org.name, "test")
            self.assertEqual(pipeline.ml_jobs.all().order_by("name")[0].owner.org.type, "dev")
            self.assertEqual(pipeline.ml_jobs.all().order_by("name")[0].owner.org.billing_plan, "free")
            self.assertEqual(pipeline.ml_jobs.all().order_by("name")[0].backend, "stream")
            self.assertEqual(pipeline.ml_jobs.all().order_by("name")[0].backend_config, {"stream_config":"dummy"})
            self.assertEqual(pipeline.ml_jobs.all().order_by("name")[0].data_view.name, "test_dataview_1")
            self.assertEqual(pipeline.ml_jobs.all().order_by("name")[0].data_view.owner.name, "test_user_1")
            self.assertEqual(pipeline.ml_jobs.all().order_by("name")[0].data_view.owner.org.name, "test")
            self.assertEqual(pipeline.ml_jobs.all().order_by("name")[0].data_view.owner.org.type, "dev")
            self.assertEqual(pipeline.ml_jobs.all().order_by("name")[0].data_view.owner.org.billing_plan, "free")

            pipeline.delete()
