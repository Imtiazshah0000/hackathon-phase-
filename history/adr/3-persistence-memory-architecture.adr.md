# ADR-3: Persistence & Memory Architecture

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together.

- **Status:** Accepted
- **Date:** 2026-03-01
- **Feature:** revops-fte
- **Context:** The Digital FTE needs to remember lead interactions, store research findings, and maintain long-term memory to prevent redundant work and ensure consistency.

## Decision

- **Primary Database:** PostgreSQL (Structured State Store)
- **Schema Strategy:** `leads`, `companies`, `conversations` (Long-term memory).
- **Audit Logging:** Detailed interaction logs for every decision made by the agent.

## Consequences

### Positive

- **Strong Persistence:** Reliable, ACID-compliant storage for business-critical lead data.
- **Relational Integrity:** Ensures company and lead data are correctly associated.
- **Interoperability:** Most CRM and data tools have robust SQL connectors.

### Negative

- **Schema Evolution:** Requires migrations as the agent's capabilities grow.
- **State Complexity:** Storing multi-step conversation context in a relational database can be complex.

## Alternatives Considered

- **Vector Database (Pinecone/Milvus):** Powerful for semantic search but less suited for the structured lead/company data used in RevOps.
- **In-Memory Store (Redis):** Fast for session memory but lacks the persistence needed for long-term lead history.

## References

- Feature Spec: [specs/revops-fte/spec.md](specs/revops-fte/spec.md)
- Implementation Plan: [specs/revops-fte/plan.md](specs/revops-fte/plan.md)
- Related ADRs: ADR-1, ADR-2
- Evaluator Evidence: none
