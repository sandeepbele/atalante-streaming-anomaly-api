from typing import Dict, List, Any, Tuple
import sqlite3

json2sqlite_types = {
        "str": "TEXT",
        "float": "REAL",
        "datetime": "TEXT",
        "bool": "INTEGER"
    }


class Aggregator:

    topics_schema:dict
    materialized_view_query:str
    view_name:str

    def __init__(self, topics_schema:dict, materialized_view_query:str, view_name:str):
        self.topics_schema = topics_schema
        self.materialized_view_query = materialized_view_query
        self.view_name = view_name

    def run(self,data:Dict[str,List[Dict[str,Any]]]):

        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()

        # create tables
        for topic in self.topics_schema:
            schema = self.topics_schema[topic]
            create_statement = f"CREATE TABLE {topic} ("
            for col in schema:
                create_statement += f"{col} {json2sqlite_types[schema[col]]},"
            create_statement = create_statement[:-1] + ");"
            print(create_statement)
            cursor.execute(create_statement)

        # insert data
        for topic in data:
            for message in data[topic]:
                print(message)

                # insert into sqlite
                insert_statement = f"INSERT INTO {topic} VALUES ("
                for col in self.topics_schema[topic]:
                    # put a quote around value if type is string
                    if json2sqlite_types[self.topics_schema[topic][col]] == "TEXT":
                        insert_statement += f"'{message[col]}',"
                    else:
                        insert_statement += f"{message[col]},"
                insert_statement = insert_statement[:-1] + ");"
                print(insert_statement)
                cursor.execute(insert_statement)

        # create view
        cursor.execute(self.materialized_view_query)

        # read schema of view
        cursor.execute(f"PRAGMA table_info({self.view_name})")

        # create dict of schema and results
        schema = {}
        for col in cursor.fetchall():
            schema[col[1]] = col[2]

        # read from hourly_anomalies and put it in dict
        cursor.execute(f"SELECT * FROM {self.view_name}")
        results = []
        for row in cursor.fetchall():
            results.append(row)

        return {"schema":schema,"results":results}


if __name__ == "__main__":

    topics = {
        "ts_metrics":{"ts":"datetime","metric":"str","value":"float"},
        "anomalies": {"ts":"datetime","metric":"str","is_anomaly":"bool"}
    }

    # write sql query that joins ts_metrics and anomalies and aggregates by hour
    materialized_view_query = "create view hourly_anomalies as " \
        "select ts_metrics.ts, ts_metrics.metric, ts_metrics.value, anomalies.is_anomaly " \
        "from ts_metrics join anomalies on ts_metrics.ts = anomalies.ts and ts_metrics.metric = anomalies.metric "

    view_name = "hourly_anomalies"

    messages = {
        "ts_metrics": [
            {"_airbyte_ab_id":"b08c0ea2-120d-47ad-acce-fd8b1ba7369d","_airbyte_stream":"ts_metrics","_airbyte_emitted_at":1687548391534,"_airbyte_data":{"metric":"error_rate","ts":"2021-08-22T18:36:00.000000Z","value":5.106428868E7}},
            {"_airbyte_ab_id":"9e2d1180-c8a2-47ca-aed8-cf31d77be765","_airbyte_stream":"ts_metrics","_airbyte_emitted_at":1687548391534,"_airbyte_data":{"metric":"error_rate","ts":"2021-08-22T18:37:00.000000Z","value":42399.6}},
            {"_airbyte_ab_id":"68ff6a9f-ab9f-48bc-b4df-73358f2cc9e5","_airbyte_stream":"ts_metrics","_airbyte_emitted_at":1687548391534,"_airbyte_data":{"metric":"error_rate","ts":"2021-08-22T18:38:00.000000Z","value":99202.35}},
            {"_airbyte_ab_id":"47780766-ab69-475a-86ea-c790ac30edaa","_airbyte_stream":"ts_metrics","_airbyte_emitted_at":1687548391534,"_airbyte_data":{"metric":"error_rate","ts":"2021-08-22T18:39:00.000000Z","value":877.0}},
            {"_airbyte_ab_id":"cf97956b-7cc6-41a4-a61d-0c13b4d94d51","_airbyte_stream":"ts_metrics","_airbyte_emitted_at":1687548391534,"_airbyte_data":{"metric":"mysql_bytes_received","ts":"2021-08-26T11:56:00.000000Z","value":2.417996223E7}},
            {"_airbyte_ab_id":"f5f9b0c2-7aab-4118-9b31-959e63ff9371","_airbyte_stream":"ts_metrics","_airbyte_emitted_at":1687548391534,"_airbyte_data":{"metric":"error_rate","ts":"2021-08-22T18:40:00.000000Z","value":0.07}}
        ],

        "anomalies": [
            {"_airbyte_ab_id":"86de8730-3e67-4692-8f9e-64ff7869c1d2","_airbyte_stream":"anomalies","_airbyte_emitted_at":1687547174021,"_airbyte_data":{"workflow":"spike_in_errors","metric":"error_rate","ts":"2021-08-22T18:36:00.000000Z","is_anomaly":True,"type":"online","score":6.306276095683733,"upper_bound":-1.0,"lower_bound":-1.0}},
            {"_airbyte_ab_id":"fa27eefd-2cfd-4117-b1ce-087d9e7709c4","_airbyte_stream":"anomalies","_airbyte_emitted_at":1687547174021,"_airbyte_data":{"workflow":"spike_in_errors","metric":"error_rate","ts":"2021-08-22T18:37:00.000000Z","is_anomaly":False ,"type":"online","score":6.489121573933899,"upper_bound":-1.0,"lower_bound":-1.0}},
            {"_airbyte_ab_id":"b08e3504-31af-4b8b-9d62-bf63a6f105aa","_airbyte_stream":"anomalies","_airbyte_emitted_at":1687547174021,"_airbyte_data":{"workflow":"spike_in_errors","metric":"error_rate","ts":"2021-08-22T18:38:00.000000Z","is_anomaly":False, "type":"online","score":6.365806957088191,"upper_bound":-1.0,"lower_bound":-1.0}},
            {"_airbyte_ab_id":"be60420b-48c8-4444-bf61-f585a46d2b98","_airbyte_stream":"anomalies","_airbyte_emitted_at":1687547174021,"_airbyte_data":{"workflow":"spike_in_errors","metric":"error_rate","ts":"2021-08-22T18:39:00.000000Z","is_anomaly":True,"type":"online","score":6.5974027676449065,"upper_bound":-1.0,"lower_bound":-1.0}}
        ]
    }

    # pre-process messages
    messages = {k: [v["_airbyte_data"] for v in messages[k]] for k in messages}

    agg = Aggregator(topics, materialized_view_query, view_name)
    agg_data = agg.run(messages)
    print(agg_data)

# [('2021-08-22T18:36:00.000000Z', 'error_rate', 51064288.68, 1), ('2021-08-22T18:37:00.000000Z', 'error_rate', 42399.6, 0), ('2021-08-22T18:38:00.000000Z', 'error_rate', 99202.35, 0), ('2021-08-22T18:39:00.000000Z', 'error_rate', 877.0, 1)]

