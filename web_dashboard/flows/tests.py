import unittest
from stream import Aggregator


class AggregatorTests(unittest.TestCase):

    def test_aggregator(self):

        topics = {
            "ts_metrics": {"ts": "datetime", "metric": "str", "value": "float"},
            "anomalies": {"ts": "datetime", "metric": "str", "is_anomaly": "bool"}
        }

        # write sql query that joins ts_metrics and anomalies and aggregates by hour
        materialized_view_query = "create view hourly_anomalies as " \
                                  "select ts_metrics.ts, ts_metrics.metric, ts_metrics.value, anomalies.is_anomaly " \
                                  "from ts_metrics join anomalies on ts_metrics.ts = anomalies.ts and ts_metrics.metric = anomalies.metric "

        view_name = "hourly_anomalies"

        messages = {
            "ts_metrics": [
                {"_airbyte_ab_id": "b08c0ea2-120d-47ad-acce-fd8b1ba7369d", "_airbyte_stream": "ts_metrics",
                 "_airbyte_emitted_at": 1687548391534,
                 "_airbyte_data": {"metric": "error_rate", "ts": "2021-08-22T18:36:00.000000Z",
                                   "value": 5.106428868E7}},
                {"_airbyte_ab_id": "9e2d1180-c8a2-47ca-aed8-cf31d77be765", "_airbyte_stream": "ts_metrics",
                 "_airbyte_emitted_at": 1687548391534,
                 "_airbyte_data": {"metric": "error_rate", "ts": "2021-08-22T18:37:00.000000Z", "value": 42399.6}},
                {"_airbyte_ab_id": "68ff6a9f-ab9f-48bc-b4df-73358f2cc9e5", "_airbyte_stream": "ts_metrics",
                 "_airbyte_emitted_at": 1687548391534,
                 "_airbyte_data": {"metric": "error_rate", "ts": "2021-08-22T18:38:00.000000Z", "value": 99202.35}},
                {"_airbyte_ab_id": "47780766-ab69-475a-86ea-c790ac30edaa", "_airbyte_stream": "ts_metrics",
                 "_airbyte_emitted_at": 1687548391534,
                 "_airbyte_data": {"metric": "error_rate", "ts": "2021-08-22T18:39:00.000000Z", "value": 877.0}},
                {"_airbyte_ab_id": "cf97956b-7cc6-41a4-a61d-0c13b4d94d51", "_airbyte_stream": "ts_metrics",
                 "_airbyte_emitted_at": 1687548391534,
                 "_airbyte_data": {"metric": "mysql_bytes_received", "ts": "2021-08-26T11:56:00.000000Z",
                                   "value": 2.417996223E7}},
                {"_airbyte_ab_id": "f5f9b0c2-7aab-4118-9b31-959e63ff9371", "_airbyte_stream": "ts_metrics",
                 "_airbyte_emitted_at": 1687548391534,
                 "_airbyte_data": {"metric": "error_rate", "ts": "2021-08-22T18:40:00.000000Z", "value": 0.07}}
            ],

            "anomalies": [
                {"_airbyte_ab_id": "86de8730-3e67-4692-8f9e-64ff7869c1d2", "_airbyte_stream": "anomalies",
                 "_airbyte_emitted_at": 1687547174021,
                 "_airbyte_data": {"workflow": "spike_in_errors", "metric": "error_rate",
                                   "ts": "2021-08-22T18:36:00.000000Z", "is_anomaly": True, "type": "online",
                                   "score": 6.306276095683733, "upper_bound": -1.0, "lower_bound": -1.0}},
                {"_airbyte_ab_id": "fa27eefd-2cfd-4117-b1ce-087d9e7709c4", "_airbyte_stream": "anomalies",
                 "_airbyte_emitted_at": 1687547174021,
                 "_airbyte_data": {"workflow": "spike_in_errors", "metric": "error_rate",
                                   "ts": "2021-08-22T18:37:00.000000Z", "is_anomaly": False, "type": "online",
                                   "score": 6.489121573933899, "upper_bound": -1.0, "lower_bound": -1.0}},
                {"_airbyte_ab_id": "b08e3504-31af-4b8b-9d62-bf63a6f105aa", "_airbyte_stream": "anomalies",
                 "_airbyte_emitted_at": 1687547174021,
                 "_airbyte_data": {"workflow": "spike_in_errors", "metric": "error_rate",
                                   "ts": "2021-08-22T18:38:00.000000Z", "is_anomaly": False, "type": "online",
                                   "score": 6.365806957088191, "upper_bound": -1.0, "lower_bound": -1.0}},
                {"_airbyte_ab_id": "be60420b-48c8-4444-bf61-f585a46d2b98", "_airbyte_stream": "anomalies",
                 "_airbyte_emitted_at": 1687547174021,
                 "_airbyte_data": {"workflow": "spike_in_errors", "metric": "error_rate",
                                   "ts": "2021-08-22T18:39:00.000000Z", "is_anomaly": True, "type": "online",
                                   "score": 6.5974027676449065, "upper_bound": -1.0, "lower_bound": -1.0}}
            ]
        }

        # pre-process messages
        messages = {k: [v["_airbyte_data"] for v in messages[k]] for k in messages}

        agg = Aggregator(topics, materialized_view_query, view_name)
        agg_data = agg.run(messages)
        print(agg_data)
        self.assertEqual(agg_data, {'schema': {'ts': 'TEXT', 'metric': 'TEXT', 'value': 'REAL', 'is_anomaly': 'INTEGER'}, 'results': [('2021-08-22T18:36:00.000000Z', 'error_rate', 51064288.68, 1), ('2021-08-22T18:37:00.000000Z', 'error_rate', 42399.6, 0), ('2021-08-22T18:38:00.000000Z', 'error_rate', 99202.35, 0), ('2021-08-22T18:39:00.000000Z', 'error_rate', 877.0, 1)]})

    def test_aggregator_pivot (self):
        "pivot data metric per row to metric value as column"

        topics = {
            "ts_metrics": {"ts": "datetime", "metric": "str", "value": "float"},
            "anomalies": {"ts": "datetime", "metric": "str", "is_anomaly": "bool"}
        }

        view_name = "ts_metrics_pivot"
        # create view by "grouping ts_metrics by ts on a minute window" and pivoting on metric
        materialized_view_query = f"""
            create view {view_name}  as SELECT strftime('%Y-%m-%d %H:%M', ts) AS ts,
                MAX(CASE WHEN metric = 'error_rate' THEN value END) AS error_rate,
                MAX(CASE WHEN metric = 'mysql_bytes_received' THEN value END) AS mysql_bytes_received,
                MAX(CASE WHEN metric = 'mysql_bytes_sent' THEN value END) AS mysql_bytes_sent
            FROM ts_metrics
            GROUP BY ts
        """

        messages = {
            "ts_metrics": [
                {"_airbyte_ab_id": "2d6f2b3d-7c2b-4c8f-9e5c-2f8d8a0b1c9f", "_airbyte_stream": "ts_metrics",
                 "_airbyte_emitted_at": 1687548391534,
                 "_airbyte_data": {"metric": "error_rate", "ts": "2021-08-26T11:56:00.000000Z",
                                   "value": 2.417996223E7}},
                {"_airbyte_ab_id": "2d6f2b3d-7c2b-4c8f-9e5c-2f8d8a0b1c9f", "_airbyte_stream": "ts_metrics",
                 "_airbyte_emitted_at": 1687548391534,
                 "_airbyte_data": {"metric": "error_rate", "ts": "2021-08-26T11:57:00.000000Z",
                                   "value": 2.417996223E7}},
                {"_airbyte_ab_id": "2d6f2b3d-7c2b-4c8f-9e5c-2f8d8a0b1c9f", "_airbyte_stream": "ts_metrics",
                 "_airbyte_emitted_at": 1687548391534,
                 "_airbyte_data": {"metric": "error_rate", "ts": "2021-08-26T11:58:00.000000Z",
                                   "value": 2.417996223E7}},
                {"_airbyte_ab_id": "2d6f2b3d-7c2b-4c8f-9e5c-2f8d8a0b1c9f", "_airbyte_stream": "ts_metrics",
                 "_airbyte_emitted_at": 1687548391534,
                 "_airbyte_data": {"metric": "error_rate", "ts": "2021-08-26T11:59:00.000000Z",
                                   "value": 2.417996223E7}},
                {"_airbyte_ab_id": "9e2d1180-c8a2-47ca-aed8-cf31d77be765", "_airbyte_stream": "ts_metrics",
                 "_airbyte_emitted_at": 1687548391534,
                 "_airbyte_data": {"metric": "error_rate", "ts": "2021-08-22T18:37:00.000000Z", "value": 42399.6}},
                {"_airbyte_ab_id": "68ff6a9f-ab9f-48bc-b4df-73358f2cc9e5", "_airbyte_stream": "ts_metrics",
                 "_airbyte_emitted_at": 1687548391534,
                 "_airbyte_data": {"metric": "error_rate", "ts": "2021-08-22T18:38:00.000000Z", "value": 99202.35}},
                {"_airbyte_ab_id": "47780766-ab69-475a-86ea-c790ac30edaa", "_airbyte_stream": "ts_metrics",
                 "_airbyte_emitted_at": 1687548391534,
                 "_airbyte_data": {"metric": "error_rate", "ts": "2021-08-22T18:39:00.000000Z", "value": 877.0}},
                {"_airbyte_ab_id": "cf97956b-7cc6-41a4-a61a-0b0b6b5b2b0e", "_airbyte_stream": "ts_metrics",
                    "_airbyte_emitted_at": 1687548391534,
                    "_airbyte_data": {"metric": "mysql_bytes_sent", "ts": "2021-08-26T11:56:00.000000Z",
                                    "value": 1.417996223E7}},
                {"_airbyte_ab_id": "b08e3504-31af-4b8b-9d62-bf63a6f105aa", "_airbyte_stream": "ts_metrics",
                    "_airbyte_emitted_at": 1687548391534,
                    "_airbyte_data": {"metric": "mysql_bytes_sent", "ts": "2021-08-26T11:57:00.000000Z",
                                    "value": 1.417996223E7}},
                {"_airbyte_ab_id": "b08e3504-31af-4b8b-9d62-bf63a6f105aa", "_airbyte_stream": "ts_metrics",
                    "_airbyte_emitted_at": 1687548391534,
                    "_airbyte_data": {"metric": "mysql_bytes_sent", "ts": "2021-08-26T11:58:00.000000Z",
                                    "value": 1.417996223E7}},
                {"_airbyte_ab_id": "b08e3504-31af-4b8b-9d62-bf63a6f105aa", "_airbyte_stream": "ts_metrics",
                    "_airbyte_emitted_at": 1687548391534,
                    "_airbyte_data": {"metric": "mysql_bytes_sent", "ts": "2021-08-26T11:59:00.000000Z",
                                    "value": 1.417996223E7}},]}

        # pre-process messages
        messages = {k: [v["_airbyte_data"] for v in messages[k]] for k in messages}

        agg = Aggregator(topics, materialized_view_query, view_name)
        agg_data = agg.run(messages)
        print(agg_data)
        self.assertEqual(agg_data, {'schema': {'ts': '', 'error_rate': '', 'mysql_bytes_received': '', 'mysql_bytes_sent': ''},
                                    'results': [('2021-08-22 18:37', 42399.6, None, None), ('2021-08-22 18:38', 99202.35, None, None),
                                                ('2021-08-22 18:39', 877.0, None, None), ('2021-08-26 11:56', 24179962.23, None, 14179962.23),
                                                ('2021-08-26 11:57', 24179962.23, None, 14179962.23), ('2021-08-26 11:58', 24179962.23, None, 14179962.23),
                                                ('2021-08-26 11:59', 24179962.23, None, 14179962.23)]})