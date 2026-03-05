# ADR-1: Core Agent Framework & Orchestration

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together.

- **Status:** Accepted
- **Date:** 2026-03-01
- **Feature:** revops-fte
- **Context:** The Digital FTE requires a robust framework for multi-step reasoning, tool-calling (research, CRM sync, outreach), and maintaining agent persona across various business functions.

## Decision

- **Framework:** OpenAI Agents SDK (Central "Brain")
- **Service Layer:** FastAPI (API Gateway & Tooling Interfaces)
- **Model Strategy:** GPT-4o for complex reasoning; GPT-4o-mini for rapid enrichment.

## Consequences

### Positive

- **Advanced Reasoning:** OpenAI Agents SDK provides a structured way to handle complex, multi-step agent logic.
- **High Performance:** FastAPI offers asynchronous processing for high-concurrency tool execution.
- **Cost Efficiency:** Using a mix of GPT-4o and GPT-4o-mini balances reasoning capabilities with token costs.

### Negative

- **Vendor Dependency:** Strong coupling with the OpenAI ecosystem and Agents SDK.
- **Complexity:** Managing state and handovers within the SDK adds implementation overhead.

## Alternatives Considered

- **LangChain/LangGraph:** Highly flexible but often comes with more abstraction overhead and a steeper learning curve for specific agentic workflows.
- **Custom Logic (vanilla FastAPI):** Provides maximum control but requires significant effort to replicate the robust tool-calling and reasoning patterns provided by the OpenAI Agents SDK.

## References

- Feature Spec: [specs/revops-fte/spec.md](specs/revops-fte/spec.md)
- Implementation Plan: [specs/revops-fte/plan.md](specs/revops-fte/plan.md)
- Related ADRs: none
- Evaluator Evidence: none
