---
id: 6
title: Task 1.1 Setup Environment and Project Structure
stage: green
date: 2026-03-01
surface: agent
model: Gemini 2.0 Flash
feature: revops-fte
branch: none
user: syedm
command: none
labels: [environment, project-structure, docker, revops, digital-fte]
links:
  spec: specs/revops-fte/spec.md
  tasks: specs/revops-fte/tasks.md
files:
 - docker-compose.yml
tests:
 - none
---

## Prompt

Let’s begin Stage 1 with Task 1.1: Setup environment and local project structure.

Please generate:
- Recommended folder structure
- Service boundaries (Gateway vs Worker)
- Environment configuration strategy
- Local development setup instructions
- Dependency grouping for FastAPI, Agent SDK, Kafka, and PostgreSQL

Ensure the structure aligns with the documented ADR decisions.

## Response snapshot

Generated a recommended folder structure separating Gateway and Worker services. Provided service boundaries, an environment configuration strategy, dependency grouping, and a `docker-compose.yml` for local infrastructure (Postgres/Kafka).

## Outcome

- ✅ Impact: Project foundation and infrastructure established for local development.
- 🧪 Tests: N/A
- 📁 Files: Created docker-compose.yml.
- 🔁 Next prompts: Task 1.2 (Mock CRM/Lead database schema) or Task 1.3 (Enrichment tools).
- 🧠 Reflection: The decoupled structure directly supports the event-driven strategy (ADR-2) and resilient deployment (ADR-4).

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
