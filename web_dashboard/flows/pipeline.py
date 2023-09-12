
# data sources
# data flows inbound
# views
# ml jobs
# data destinations (topics)
# data flows outbound

# data sources
## add data source: kafka, postgres etc.

# data flows
## new data flow: <data_source> <> Kafka(always)

# views
## new view: [data_flows] -> query [aggregate from multiple data flows]

# ml jobs
## new ml job: input is view -> output is topic

# data destinations
# list of ml output topics

# data flows outbound
# new data flow: <topic> -> <data_destination>



