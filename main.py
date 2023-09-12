# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from kafka import KafkaConsumer

# write a code to read from kafka topic, parse message into pydantic model and call anomaly detection function for each message in the topic
# anomaly detection function will be called with the parsed message as input
# anomaly detection function will return a boolean value indicating if the message is an anomaly or not
# if the message is an anomaly, the anomaly detection function will write the message to a kafka topic
# if the message is not an anomaly, the anomaly detection function will write the message to a kafka topic
# kafka topic to write anomalies to is called anomaly
# kafka topic to write non-anomalies to is called non-anomaly


from kafka import KafkaConsumer, KafkaProducer, KafkaAdminClient
from pydantic import BaseModel
import json
from datetime import datetime

from pydantic.class_validators import validator
from river.compose import Pipeline
from river.anomaly import HalfSpaceTrees, OneClassSVM
from river.preprocessing import MinMaxScaler, StandardScaler
from river import feature_extraction as fx
from typing import Dict

# Define Pydantic data model
class TSModel(BaseModel):
    ts: datetime
    metric: str
    value: float

    class Config:
        json_encoders = {
                            datetime: lambda v: v.isoformat()
        }

    def to_features(self):
        features = self.dict()
        features['day'] = self.ts.day
        features['day_of_week'] = self.ts.isoweekday()
        features['hour'] = self.ts.hour
        features['minute'] = self.ts.minute
        features['is_weekend'] = self.ts.isoweekday() in [6,7]
        features['month'] = self.ts.month

        features.pop('ts')
        return features



class RiverANDetector:

    model_zoo = {
        'hs_tree': Pipeline(('scale', MinMaxScaler()), ('detector', HalfSpaceTrees())),
        'hs_tree_with_feature': Pipeline(('scale', MinMaxScaler()), (fx.PolynomialExtender()),
                                                 ('detector', HalfSpaceTrees())),
        'hs_tree_with_feature_d2': Pipeline(('scale', MinMaxScaler()),
                                                    (fx.PolynomialExtender(degree=2, include_bias=True)),
                                                    ('detector', HalfSpaceTrees())),
        'hs_tree_with_feature_d2_rbf': Pipeline(('scale', MinMaxScaler()),
                                                        (fx.PolynomialExtender(degree=3, include_bias=True)),
                                                        ('sampler', fx.RBFSampler()), ('detector', HalfSpaceTrees())),
        'svm_with_scalar_rbf': Pipeline(('scale', StandardScaler()), ('sampler', fx.RBFSampler()),
                                                ('detector', OneClassSVM()))
    }

    def __init__(self,metric:str , model_config:str=None):

        if model_config is None:
            self.model = self.model_zoo['hs_tree']
        else:
            self.model = self.model_zoo[model_config]

        self.metric = metric
        self.anomaly_threshold = 0.7

    def detect_anomaly(self, ts_point:TSModel):
        score = self.model.score_one({'x':ts_point.value})
        self.model = self.model.learn_one({'x':ts_point.value})

        is_anomaly = False
        if score > self.anomaly_threshold:
            is_anomaly = True

        return ts_point,is_anomaly,score


# Kafka consumer configuration
consumer_topic = 'elastic_sync'
consumer_group_id = 'my_consumer'

# Kafka producer configuration
producer_topic_anomaly = 'anomaly'
producer_topic_non_anomaly = 'non-anomaly'
consumer = KafkaConsumer(consumer_topic,
                         group_id=consumer_group_id,
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('ascii')),
                         auto_offset_reset='earliest')


def serialize_ts(value):
    if isinstance(value, datetime):
        return value.isoformat()
    return value

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda m: json.dumps(m, default=serialize_ts ).encode('ascii'))

models_cache: Dict[str,RiverANDetector] = {}

for message in consumer:
    data = TSModel.parse_obj(message.value['_airbyte_data'])
    if data.metric not in models_cache:
        models_cache[data.metric] = RiverANDetector(data.metric,'hs_tree_with_feature')

    model = models_cache[data.metric]

    data,is_anomaly,score =  model.detect_anomaly(data)
    if is_anomaly:
        producer.send(producer_topic_anomaly, value={'data':data.dict(),'score':score})
    else:
        producer.send(producer_topic_non_anomaly, value={'data':data.dict()})


from river.base.typing import Stream
from typing import Callable


def parse_tsmodel(message):
    data = TSModel.parse_obj(message.value['_airbyte_data'])
    return data.to_features()

# parse_message is a function that takes a message and returns a dict
# parse_message = lambda x: json.loads(x.value.decode('utf-8'))
def iter_kafka( topic:str,
                bootstrap_servers:list=["localhost:9092"],
                auto_offset_reset:str='earliest',parse_message:Callable=None )-> Stream:

    #consumer = KafkaConsumer('elastic_sync', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest')
    consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, auto_offset_reset=auto_offset_reset)
    for message in consumer:
        # parse json message into pydantic model
        yield parse_message(message),None if parse_message is not None else message.value,None





'''
def test_kafka():
    consumer = KafkaConsumer('elastic_sync', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest')
    #consumer = KafkaConsumer('elastic_sync', bootstrap_servers=['localhost:9092'])
    for message in consumer:
        # parse json message into pydantic model
        print (message)


# create pydantic model to read from kafka topic and parse the message into a python object
from pydantic import BaseModel
from pendulum import datetime

class Message(BaseModel):
     ts: datetime
     data : dict[str:float]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_kafka()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
'''