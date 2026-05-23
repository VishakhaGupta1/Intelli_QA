# Production Monitoring

Use any Prometheus-compatible scraper to collect metrics from `https://your-domain/metrics`. The dashboard API exposes the metrics endpoint only to trusted internal IPs, so the scraper must run inside your private network, VPC, or an allowlisted egress range.

## Access Model

- Expose `GET /metrics` only behind an internal load balancer, VPN, reverse proxy allowlist, or private network route.
- Keep `METRICS_ALLOWED_SUBNETS` restricted to scraper IPs and internal ranges only.
- Do not publish the metrics endpoint publicly without an IP allowlist.

## Recommended Alerts

Use these PromQL expressions directly in your alert rules:

- `qa_api_duration_seconds{quantile="0.95"} > 0.5` → HIGH latency alert
- `rate(qa_api_requests_total{status=~"5.."}[5m]) > 0.01` → error rate alert
- `qa_test_results_total == 0` → no data alert
- `up{job="qa-dashboard-api"} == 0` → service down alert

## Grafana Cloud

Grafana Cloud is the quickest managed option for teams that want hosted dashboards and alerting without operating their own Grafana stack. Start here: https://grafana.com/products/cloud/

Point Grafana Cloud's Prometheus-compatible scraper at your `https://your-domain/metrics` endpoint, then import the dashboard JSON from `monitoring/grafana/dashboards/qa-platform.json` or recreate the panels in your cloud workspace.

## AWS Managed Prometheus

If you run on AWS, use Amazon Managed Service for Prometheus to scrape the same metrics endpoint through a private integration or VPC-accessible target. Pair it with Amazon Managed Grafana or your own Grafana deployment.

Recommended setup:

1. Expose the dashboard API through an internal AWS load balancer or service discovery name.
2. Allow the AMP scraper IPs or VPC ranges in `METRICS_ALLOWED_SUBNETS`.
3. Import the dashboard JSON into Grafana and wire the Prometheus data source to AMP.
4. Reuse the alert expressions above in AMP or Grafana Alerting.