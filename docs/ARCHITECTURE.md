# Architecture

## Design Principles

1. Read-only investigation by default.
2. Evidence before conclusions.
3. Provider adapters isolate external systems.
4. AI produces hypotheses and explanations, not unchecked operational actions.
5. Every investigation should be reproducible.

## Investigation Flow

```text
Alert
  |
  v
Incident API
  |
  v
Investigation Orchestrator
  |
  +--> Kubernetes Adapter
  +--> Prometheus Adapter
  +--> Loki Adapter
  +--> OpenTelemetry Adapter
  +--> GitHub Adapter
  |
  v
Evidence Store
  |
  v
LLM Investigator
  |
  v
Root Cause + Confidence + Evidence
  |
  v
Human Approval
  |
  v
Optional Remediation
```
