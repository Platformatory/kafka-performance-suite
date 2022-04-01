A Helm chart to run CFK benchmarks.

# Prerequisites

## Infrastructure

1. A CNCF Kubernetes cluster
2. A domain name to map ingress DNS to Kafka brokers.

## Tools

### Confluent Kubernetes operator

Confluent Kubernetes operator. **NOTE** that this has to be configured to listen in all namespaces.

### Nginx ingress controller

Inginx ingress controller which is configured with TLS passthrough.


### Prometheus and Grafana

Prometheus and Grafana already setup in the cluster.

# Installing this Helm chart

```
cd ..
helm upgrade --install pf ./confluent-performance-suite
```

This chart is not yet deployed to a Helm repository.

# What the chart does

This chart creates a topic in the configured confluent cluster and runs one or more producers and consumers to produce and consume messages on the topic. The pods print the JMX metrics and run forever until they are deleted manually.

There is also an optional end to end latency test pod which can be deployed.

