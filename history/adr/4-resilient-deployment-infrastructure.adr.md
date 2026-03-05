# ADR-4: Resilient Deployment & Infrastructure

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together.

- **Status:** Accepted
- **Date:** 2026-03-01
- **Feature:** revops-fte
- **Context:** The Digital FTE must be a production-grade, 24/7 autonomous employee deployed at scale with zero downtime and resilient recovery.

## Decision

- **Orchestration:** Kubernetes (Deployment Strategy)
- **Containerization:** Docker (Isolated environments for Gateway and Worker)
- **Scaling Strategy:** Horizontal Pod Autoscaler (HPA) for handling high lead volume.
- **Monitoring/Observability:** Prometheus/Grafana (Metrics) + ELK Stack (Logging).

## Consequences

### Positive

- **High Availability:** Auto-healing and rolling updates ensure the agent is always online.
- **Elastic Scalability:** Pods automatically scale up to handle sudden lead spikes.
- **Enterprise-Ready:** Follows standard cloud-native deployment patterns.

### Negative

- **Operational Overhead:** Managing Kubernetes clusters (or managed services) requires significant DevOps knowledge.
- **Resource Consumption:** Control plane and monitoring add infrastructure costs.

## Alternatives Considered

- **Serverless (AWS Lambda/Google Cloud Functions):** Easy to scale but less suited for the long-running reasoning loops used by the Agent SDK.
- **Single VM (Docker Compose):** Simplifies deployment but lacks the scaling and resilience of Kubernetes.

## References

- Feature Spec: [specs/revops-fte/spec.md](specs/revops-fte/spec.md)
- Implementation Plan: [specs/revops-fte/plan.md](specs/revops-fte/plan.md)
- Related ADRs: ADR-1, ADR-2, ADR-3
- Evaluator Evidence: none
