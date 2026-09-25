from channels.generic.websocket import AsyncWebsocketConsumer
#from confluent_kafka import Consumer, KafkaException
from kafka import KafkaConsumer
from kafka.errors import KafkaError

import json
import asyncio


class KafkaStreamer(AsyncWebsocketConsumer):

    c = None

    async def setup(self):
        await super().setup()
        await self.connect()

    async def connect(self):

        await self.accept()

        topic_name = self.scope['url_route']['kwargs']['topic_name']


        c = KafkaConsumer(topic_name,
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
            consumer_timeout_ms=1000,
            group_id='websocket_consumer_2',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')))

        #c.subscribe([topic_name])

        while True:
            try:
                '''msg = c.poll(1.0)

                if msg is None or msg == {}:
                    continue
                else:
                    # Push the message value to the WebSocket
                    await self.send(text_data=json.dumps({'message': msg}))
                '''
                for msg in c.poll(1.0):
                    await self.send(text_data=json.dumps(msg.value['_airbyte_data']))

                for msg in c:
                    await self.send(text_data=json.dumps(msg.value['_airbyte_data']))


            except KafkaError as e:
                # Handle Kafka exceptions
                print(e)
                c.close()

            await asyncio.sleep(0.1)  # to prevent the loop from running too fast

    async def disconnect(self, close_code):
        super.disconnect(close_code)
        if self.c is not None:
            self.c.close()