from kafka import KafkaConsumer
import concurrent.futures
import json
from typing import Dict
from datetime import datetime
from kafka import KafkaProducer

from mlhub import RiverANDetector, TSModel

models_cache: Dict[str, RiverANDetector] = {}


def detect_anomaly(message):
    data = TSModel.parse_obj(message.value['_airbyte_data'])
    if data.metric not in models_cache:
        models_cache[data.metric] = RiverANDetector(data.metric, 'hs_tree_with_feature')

    model = models_cache[data.metric]

    data, is_anomaly, score = model.detect_anomaly(data)

    return data, is_anomaly, score


def process_data(message):
    # CPU intensive process goes here
    print("Processing:", message)


def serialize_ts(value):
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def consume(topic_from):

    #topic_from = kwargs['topic_from']
    #topic_to = kwargs['topic_to']
    topic_to = 'ts_metrics_an'

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda m: json.dumps(m, default=serialize_ts).encode('ascii'))

    consumer = KafkaConsumer(
        topic_from,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        group_id="consumer-group-a-1",
        value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    print("Consuming:", topic_from)

    # Consume messages
    for msg in consumer:

        data, is_anomaly, score = detect_anomaly(msg)

        if is_anomaly:
            producer.send(topic_to, value={'data': data.dict(), 'score': score})
        else:
            #producer.send(producer_topic_non_anomaly, value={'data': data.dict()})
            print("Non-anomaly:", data.dict())

    consumer.close()


with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    # Assuming there are 4 kafka topics
    #topics = ['my-topic-1', 'my-topic-2', 'my-topic-3', 'my-topic-4']
    #topics = [{'topic_from':'ts_metrics','topic_to':'ts_metrics_an'},
    #          {'topic_from':'elastic_sync','topic_to':'elastic_sync_an'}]
    topics = ['ts_metrics','elastic_sync']

    try:
        executor.map(consume, topics)
    except Exception as e:
        print(e)
    executor.shutdown(wait=True)
