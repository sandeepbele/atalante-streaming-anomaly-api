from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('my_view', views.my_view, name='my_view'),
    path('sources', views.show_sources, name='show_sources'),
    path('configure_source', views.configure_source, name='configure_source'),
    path('show_schema/<source_id>', views.show_schema, name="show_schema"),
    path('show_schedule', views.show_schedule, name="show_schedule"),
    path('setup_sync', views.setup_sync, name="setup_sync"),
    path('test_table_form', views.test_table_form, name="test_table_form"),
    path('sync_status', views.sync_status, name="sync_status"),
    path('tail_q/<topic_name>/<consumer_group>', views.tailf_kafka, name="tailf_kafka"),
    path('select_ml', views.select_ml_process, name="select_ml"),
    path('select_destination', views.select_destination, name="select_destination"),
    path('view_pipeline', views.view_pipeline, name="view_pipeline"),
    path('fp_validate', views.fp_validate, name="fp_validate"),
]