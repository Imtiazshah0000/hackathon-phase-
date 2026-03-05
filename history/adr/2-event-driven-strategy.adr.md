# ADR-2: Event-Driven Communication Strategy

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together.

- **Status:** Accepted
- **Date:** 2026-03-01
- **Feature:** revops-fte
- **Context:** Decoupling intake from complex agent reasoning is essential to ensure 24/7 reliability and the ability to process multiple leads without blocking.

## Decision

- **Message Broker:** Kafka (Reliability & Persistence)
- **Producers/Consumers:** Decoupled FastAPI (Intake) and Agent Workers (Processing).
- **Topic Strategy:** `lead.ingested`, `lead.enriched`, `lead.qualified`, `outreach.dispatched`.

## Consequences

### Positive

- **Fault Tolerance:** If an agent worker pod restarts, no lead is lost in Kafka.
- **Scalability:** The system can easily scale up workers based on Kafka consumer lag.
- **Auditability:** Kafka topics provide a durable log of every lead's lifecycle.

### Negative

- **Infrastructure Complexity:** Managing and maintaining a Kafka cluster (or using a managed service) adds operational overhead.
- **Message Latency:** Small overhead introduced by producing/consuming events between services.

## Alternatives Considered

- **Redis Streams/PubSub:** Simpler to manage but less durable for long-lived lead processing tasks.
- **FastAPI Background Tasks:** No persistence; if the service restarts, pending tasks are lost.

## References

- Feature Spec: [specs/revops-fte/spec.md](specs/revops-fte/spec.md)
- Implementation Plan: [specs/revops-fte/plan.md](specs/revops-fte/plan.md)
- Related ADRs: ADR-1
- Evaluator Evidence: none
