from river.base.typing import Stream
from typing import Callable
from kafka import KafkaConsumer
from pydantic import BaseModel
from datetime import datetime
import json

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


def parse_tsmodel(message):
    data = TSModel.parse_obj(message.value['_airbyte_data'])
    return data.to_features()

# parse_message is a function that takes a message and returns a dict
# parse_message = lambda x: json.loads(x.value.decode('utf-8'))
def iter_kafka( topic:str,
                bootstrap_servers:list=["localhost:9092"],
                auto_offset_reset:str='earliest',parse_message:Callable=None )-> Stream:

    #consumer = KafkaConsumer('elastic_sync', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest')
    consumer = KafkaConsumer(topic,
                             bootstrap_servers=bootstrap_servers,
                             auto_offset_reset=auto_offset_reset,
                             value_deserializer=lambda m: json.loads(m.decode('ascii')))

    for message in consumer:
        # parse json message into pydantic model
        if parse_message is not None:
            yield parse_message(message),None
        else:
            yield message.value,None


if __name__ == '__main__':
    count = 0
    for message in iter_kafka('elastic_sync', parse_message=parse_tsmodel):
        print (message)
        count += 1
        if count == 10: break

