# AI SRE Copilot

AI-powered incident investigation and SRE assistant for production cloud-native workloads.

## Portfolio Goal

AI SRE Copilot demonstrates how an FDE / Cloud / Platform Engineer can:

- operate production workloads
- correlate metrics, logs, traces, deployments and Git changes
- investigate incidents
- produce evidence-backed root-cause analysis
- recommend safe remediation
- document incidents and runbooks

## Architecture

```text
Alerts / User
      |
      v
 FastAPI API
      |
      +--------------------+
      |                    |
      v                    v
Incident Engine       AI Investigator
      |                    |
      +----------+---------+
                 |
       +---------+---------+
       |         |         |
       v         v         v
 Kubernetes  Prometheus   Loki
       |         |         |
       +---------+---------+
                 |
            OpenTelemetry
                 |
               Traces

GitHub / Deployments ---> Change Correlation
                 |
                 v
          Incident Report
```

## Planned Stack

- Python / FastAPI
- Kubernetes
- Prometheus
- Grafana
- Loki
- OpenTelemetry
- Docker
- Terraform
- Helm
- GitHub Actions
- PostgreSQL
- Redis
- LLM API with tool calling

## Repository Status

This repository is an MVP scaffold. The implementation is intentionally organized into layers so infrastructure, observability and AI investigation can be added incrementally.

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

API health check:

```bash
curl http://localhost:8000/health
```

API documentation:

```text
http://localhost:8000/docs
```

## Example Incident

```text
API latency > 2 seconds
        |
        v
Check Kubernetes
Check pod restarts
Check CPU / memory
Check Prometheus metrics
Check logs
Check traces
Check recent deployment
        |
        v
Evidence
        |
        v
Root Cause
        |
        v
Recommended Remediation
```

## FDE Case Study

A future case study should document:

1. Customer requirements
2. Architecture decisions
3. Deployment
4. Observability
5. Failure simulation
6. Investigation
7. Root-cause analysis
8. Remediation
9. Post-incident report
10. Lessons learned

## Safety

The MVP is read-only by default. Remediation actions should require explicit approval and should never execute arbitrary commands from an LLM.
