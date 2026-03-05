---
id: 9
title: Task 1.4 Define Agent Persona and Qualification Logic
stage: green
date: 2026-03-01
surface: agent
model: Gemini 2.0 Flash
feature: revops-fte
branch: none
user: syedm
command: none
labels: [persona, logic, reasoning, revops, digital-fte]
links:
  spec: specs/revops-fte/spec.md
  tasks: specs/revops-fte/tasks.md
  adr: history/adr/1-core-agent-framework.adr.md
files:
 - shared/tools/logic.py
 - shared/tests/test_logic.py
tests:
 - shared/tests/test_logic.py
---

## Prompt

Proceed with Task 1.4: Define the Agent Persona & Qualification Logic.

Please generate:
- Agent persona (tone, role, decision style)
- Lead qualification rules and scoring thresholds
- Escalation conditions for human intervention
- Example reasoning flows for common lead scenarios
- Integration points with the enrichment tools and mock CRM

Ensure the logic aligns with the RevOps Digital FTE ADRs and supports smooth Stage 2 integration with the OpenAI Agents SDK.

## Response snapshot

Defined the "Alex" agent persona and implemented BANT-enhanced qualification logic in `shared/tools/logic.py`. Established scoring thresholds, escalation triggers for human intervention, and validated the reasoning flows with a test suite in `shared/tests/test_logic.py`.

## Outcome

- ✅ Impact: The "brain" of the Digital FTE is now functionally defined and testable.
- 🧪 Tests: Created shared/tests/test_logic.py.
- 📁 Files: Created shared/tools/logic.py and shared/tests/test_logic.py.
- 🔁 Next prompts: Task 2.1 (OpenAI Agents SDK integration) or Task 1.5 (Validation Sprint).
- 🧠 Reflection: Defining escalation triggers early ensures the agent remains safe and reliable during its autonomous operations in Stage 2.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
