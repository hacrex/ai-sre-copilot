# SRE Runbook

## High API Latency

1. Check service health.
2. Check pod restarts.
3. Check CPU and memory.
4. Check request rate and error rate.
5. Check database connection saturation.
6. Inspect logs for timeout/error patterns.
7. Inspect distributed traces.
8. Check recent deployments.
9. Form a hypothesis from multiple signals.
10. Validate the hypothesis before remediation.

## Pod OOMKilled

1. Check memory requests/limits.
2. Check historical memory usage.
3. Identify affected workload version.
4. Inspect application logs.
5. Check whether traffic changed.
6. Review recent code/config changes.
7. Increase capacity only after confirming the cause.
