# Atalante

**Streaming Anomaly Detection**

Atalante was an experiment in detecting unusual events as a time series arrives, rather than repeatedly training a forecasting model on a batch of historical data. A stream of request rates, sensor readings, or infrastructure metrics keeps changing. The idea was to connect those streams, combine the signals that belong together, and let a model update as each observation passes through.

The project grew out of the earlier [Eunomia](https://github.com/sandeepbele/eunomia-anomaly-api) experiment. Eunomia put a forecasting model behind an anomaly-detection API: train on history, then compare new values with forecast intervals. Atalante explored a different direction: online learning with [River](https://riverml.xyz/) and a pipeline that can work with events from multiple sources.

## What is in the code

- **Airbyte integration and a Django dashboard** for configuring sources and viewing pipeline state (`web_dashboard/airbyte_helper.py`, `web_dashboard/views.py`, and the templates).
- **Kafka ingestion and output** for metric events (`web_dashboard/taskmaster.py` and `web_dashboard/kafka_helper.py`).
- **In-memory SQLite aggregation** to join and reshape events from several topics before they reach a model (`web_dashboard/flows/stream.py`).
- **River anomaly detectors** that score an observation and then learn from it (`web_dashboard/mlhub.py` and `web_dashboard/flows/ml/mlprocessor.py`). The code experiments with Half-Space Trees, One-Class SVM, scaling, and time-derived features.
- **Pipeline and job models** that sketch how sources, views, ML jobs, and destinations could be connected (`web_dashboard/models.py` and `web_dashboard/flows/`).

The core path is:

```text
source → Airbyte/Kafka → join or reshape observations → River score → update model → anomaly event
```

For example, a Kafka message containing a metric, timestamp, and value is parsed into `TSModel`. `taskmaster.py` sends it to `RiverANDetector`, which calculates a score before learning that observation. If the score exceeds the prototype's threshold, the consumer publishes an event to its anomaly topic. The aggregation code separately shows how streams can be joined by timestamp and metric, or pivoted into a wider set of features.

## Why streaming?

Batch forecasting works well when a series can be trained on a known history and checked later. For high-volume or changing data, I wanted to explore a system that could accept observations continuously and adapt without an application scheduling model retraining. I also wanted to detect patterns across related signals, rather than treating every metric as an isolated column.

This repository captures those experiments. The dashboard and pipeline definitions are prototypes; it does not expose a completed anomaly-detection HTTP API despite the repository name.

## Inspect a small working part

The SQLite aggregation tests use only the Python standard library. From the repository root:

```bash
cd web_dashboard/flows
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests
```

The full Airbyte, Kafka, Django, and River pipeline needs historical services and dependencies and has not been revalidated for this archive.

## Note

This project is archived. It preserves a 2023 exploration of streaming anomaly detection, not a maintained service. The public history retains the original commit dates; three committed scratchpads and a Django development key were removed from the public copy. See [HISTORY.md](HISTORY.md).
