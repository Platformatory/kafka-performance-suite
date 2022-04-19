A Helm chart to run CFK benchmarks.

# Prerequisites

## Infrastructure

1. A CNCF Kubernetes cluster

## Tools

### Prometheus and Grafana

Prometheus and Grafana already setup in the cluster. If not, enable them as a dependency in current helm chart.

### Confluent cloud

Setup a confluent cloud account which will be used t

### Confluent Kubernetes operator(optional)

Confluent Kubernetes operator. **NOTE** that this has to be configured to listen in all namespaces. This is required only if we are benchmarking the client with a CFK cluster.

### Nginx ingress controller(optional)

Inginx ingress controller which is configured with TLS passthrough. This is required only if we are benchmarking the client with a CFK cluster.

# Installing this Helm chart

```
helm upgrade --install pf ./confluent-performance-suite
```

# What the chart does

This chart creates a topic in the configured confluent cluster and runs one or more producers and consumers to produce and consume messages on the topic. The pods print the JMX metrics and run forever until they are deleted manually.

There is also an optional end to end latency test pod which can be deployed.

This chart has a batteries-included Pormetheus and Grafana setup which imports the JMX metrics from the client pods automatically.
