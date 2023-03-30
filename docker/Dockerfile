FROM confluentinc/cp-kafka:7.3.2

COPY jmx /usr/app
# Install Prometheus
RUN curl -s https://api.github.com/repos/prometheus/prometheus/releases/latest \
  | grep browser_download_url \
  | grep linux-amd64 \
  | cut -d '"' -f 4 \
  | wget -qi - && \
  tar xf prometheus*.tar.gz && \
  cd prometheus*/ && \
  mv prometheus ..



