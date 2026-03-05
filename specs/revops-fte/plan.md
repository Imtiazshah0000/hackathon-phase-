# Architectural Plan: RevOps Digital FTE (Stage 2 Specialization)

## 1. High-Level Architecture
A production-grade, event-driven, autonomous AI employee deployed on Kubernetes.

## 2. Components

### A. OpenAI Agents SDK Integration
- **Role:** Central "Brain" (Orchestrator).
- **Function:** Handles multi-step reasoning, tool-calling (research, CRM sync, outreach), and maintaining agent persona.
- **Model:** GPT-4o or o1-preview for complex reasoning; GPT-4o-mini for fast enrichment.

### B. FastAPI Service Layer
- **Role:** API Gateway & Tooling Interfaces.
- **Function:** 
  - Receives webhooks (Slack, Email).
  - Exposes "Tools" for the Agent SDK (e.g., `update_crm`, `search_linkedin`, `send_email`).
  - Manages authentication (OAuth2) and logging.

### C. PostgreSQL (Persistence & Memory)
- **Role:** Structured Memory & State Store.
- **Function:**
  - **Lead Management:** `leads`, `companies`, `conversations` tables.
  - **Agent State:** Store long-term memory, user preferences, and historical qualification decisions.
  - **Audit Logs:** Track every decision made by the Digital FTE.

### D. Kafka (Event-Driven Processing)
- **Role:** Message Broker & Task Queue.
- **Function:** 
  - **Decoupling:** Decouples intake (FastAPI) from heavy processing (Agent SDK).
  - **Reliability:** Ensures no lead is lost if the agent service restarts.
  - **Topics:** `lead.ingested`, `lead.researched`, `lead.qualified`, `outreach.dispatched`.

### E. Kubernetes (Deployment Strategy)
- **Role:** Orchestration & Scaling.
- **Function:**
  - **Deployments:** Scalable replicas for the FastAPI gateway and Agent worker pods.
  - **StatefulSets:** Managed PostgreSQL or connection to a managed Cloud SQL instance.
  - **Secrets:** Kubernetes Secrets for OpenAI API keys, CRM credentials, and DB strings.
  - **Liveness/Readiness Probes:** Ensure 24/7 availability with auto-restarts.

## 3. Data Flow
1. **Intake:** Webhook (Slack/Email) -> FastAPI -> Produce to Kafka topic `lead.ingested`.
2. **Processing:** Agent Worker consumes `lead.ingested` -> Research (Tools) -> Qualification (Logic) -> Produce to `lead.qualified`.
3. **Action:** Agent Worker consumes `lead.qualified` -> Update PostgreSQL/CRM -> Outreach (Tools) -> Notify human via Slack.
4. **Monitoring:** Prometheus/Grafana dashboard tracking leads/hour, success rates, and token costs.

## 4. Security & Compliance
- **TLS:** All traffic encrypted in transit.
- **VPC:** Internal services (Kafka, DB) isolated from public internet.
- **RBAC:** Fine-grained access control for agent tool execution.
