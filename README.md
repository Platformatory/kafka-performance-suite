A Helm chart to run Kafka benchmarks.

# Motivation

We surveyed a existing kafka benchmarking tools like Openmessaging benchmark, Apache Trogdor, Jmeter etc. and identified limitations in their approaches which didn't fit our requirements, like:

1. Ease of setup and teardown.
2. Ability to visualize metrics data
3. Simulation of real-life scenarios to the extent possible

This Helm chart runs kafka-perf tools in a clound native setting with configurable parameters, and streams the results to Prometheus & Grafana, in addition to writing the metrics data to a pre-configured S3 bucket.

# Prerequisites

## Infrastructure

1. A Kubernetes cluster

## Tools

### Prometheus and Grafana

To setup Prometheus and Grafana in your cluster, install the helm chart which will setup both services along with Kafka producer and consumer dashboards.

```sh
helm upgrade --install prom-stack ./kube-prometheus-kafka-chart -n kafka-benchmarks
```



**NOTE** that this is optional and required only if you want to visualize your metrics in Grafana. We highly recommend it.

# Installing this Helm chart

```sh
helm install perf-metrics-scenario-1 ./kafka-performance-metrics-chart -n kafka-benchmarks
```

# What the chart does

This chart creates a topic in the configured confluent cluster and runs one or more producers and consumers to produce and consume messages on the topic. The pods print the JMX metrics and run forever until they are deleted manually.

There is also an optional end to end latency test pod which can be deployed.

This chart has a batteries-included Pormetheus and Grafana setup which imports the JMX metrics from the client pods automatically.

Finally, it can also be configured to pipe out metrics to any OpenMetrics compatible service, like New Relic.

Every test run is a sequence of Helm chart installation, writing metrics data to Prometheus via and teardown by deleting the Helm chart.

Example scenario to run 3 producers and single consumer:

```
topic: 
  name: "t1_benchmark"
  replicationFactor: 3
  partitions: 1

broker:
  url: "broker-url.confluent.cloud:9092"
  username: "RANDOMSTRING"
  password: "AnotherRandomString123/$"

producer:
  enabled: true
  image: "confluentinc/cp-kafka:7.0.1"
  recordsCount: 1000
  recordSizeBytes: 1024
  throughput: "-1"
  acks: 1
  count: 3
  params: "batch.size=100000 linger.ms=100 compression.type=lz4"

consumer:
  enabled: true
  image: "confluentinc/cp-kafka:7.0.1"
  messagesCount: 1000
  count: 1
  timeout: 100000

e2e:
  enabled: false

prometheus:
  remote_write:
  - url: "http://prom-stack-kube-prometheus-prometheus:9090/api/v1/write"
```

The above is a sample Helm chart values file to run this scenario. After running the scenario, the metrics will be written to the in-cluster Prometheus service.


## Chart parameters

### Common parameters

| Name                     | Description                                                                             | Value           |
| ------------------------ | --------------------------------------------------------------------------------------- | --------------- |
| `s3.accessKey`            | The AWS Access key required to write to S3 bucket.                                                             | `""`            |
| `s3.secretKey`           | The AWS Secret key required to write to S3 bucket.                                      | `""`            |
| `s3.testPrefix`       | The name of the scenario in snake-case. This will be the prefix for generated directory when storing in S3.                                          | `""`            |
| `s3.bucket`          | S3 bucket name.                                                       | `""` |


## Custom container image

There is a provision to build a custom container image to run the metrics. In our case, we added the Prometheus JMX Java agent and the prometheus binary to the base Confluent image. The idea is to run the Producer and Consumer jobs in push mode, where the Prometheus agent fetches metrics from JMX java agent and ships it off to the Prometheus server.
