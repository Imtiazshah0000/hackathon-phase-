import asyncio
import json
from typing import List, Dict, Any
from ..tools.logic import revops_logic
from ..models.leads import LeadBase

# 1. Golden Dataset: Mock leads with expected outcomes
GOLDEN_DATASET = [
    {
        "input": {
            "first_name": "John",
            "last_name": "Doe",
            "email": "j.doe@acme.corp",
            "job_title": "VP of Sales",
            "company_name": "Acme Corp"
        },
        "expected": {
            "action": "AUTO_QUALIFY",
            "min_score": 70,
            "escalate": False
        }
    },
    {
        "input": {
            "first_name": "Sarah",
            "last_name": "Connor",
            "email": "s.connor@cyberdyne.io",
            "job_title": "Head of Security",
            "company_name": "CyberDyne Systems"
        },
        "expected": {
            "action": "AUTO_QUALIFY",
            "min_score": 70,
            "escalate": False
        }
    },
    {
        "input": {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "j.smith@acme.corp",
            "job_title": "Sales Associate",
            "company_name": "Acme Corp"
        },
        "expected": {
            "action": "MANUAL_REVIEW",
            "min_score": 40,
            "escalate": True
        }
    },
    {
        "input": {
            "first_name": "Bob",
            "last_name": "Builder",
            "email": "bob@smallbiz.com",
            "job_title": "Owner",
            "company_name": "Bob's Construction"
        },
        "expected": {
            "action": "DISCARD",
            "max_score": 39,
            "escalate": False
        }
    },
    {
        "input": {
            "first_name": "Alice",
            "last_name": "Vance",
            "email": "alice@blackmesa.com",
            "job_title": "Strategic request for human contact",
            "company_name": "Black Mesa"
        },
        "expected": {
            "escalate": True
        }
    }
]

async def run_validation_sprint():
    results = []
    print(f"🚀 Starting Validation Sprint for Stage 1 Digital FTE...")
    print(f"-------------------------------------------------------")

    for i, test_case in enumerate(GOLDEN_DATASET):
        lead = LeadBase(**test_case["input"])
        expected = test_case["expected"]
        
        # Process lead through the agent logic
        actual = await revops_logic.process_lead_reasoning(lead)
        
        # Validation checks
        passed = True
        errors = []

        if "action" in expected and actual["action"] != expected["action"]:
            passed = False
            errors.append(f"Expected action {expected['action']}, got {actual['action']}")
        
        if "min_score" in expected and actual["score"] < expected["min_score"]:
            passed = False
            errors.append(f"Score {actual['score']} below min {expected['min_score']}")

        if "max_score" in expected and actual["score"] > expected["max_score"]:
            passed = False
            errors.append(f"Score {actual['score']} above max {expected['max_score']}")

        if actual["escalate_to_human"] != expected["escalate"]:
            passed = False
            errors.append(f"Escalation mismatch: expected {expected['escalate']}, got {actual['escalate_to_human']}")

        status = "PASS" if passed else "FAIL"
        print(f"Lead {i+1}: {lead.first_name} {lead.last_name} ({lead.company_name}) -> {status}")
        
        results.append({
            "lead": f"{lead.first_name} {lead.last_name}",
            "status": status,
            "actual": actual,
            "errors": errors
        })

    return results

def generate_report(results: List[Dict[str, Any]]):
    total = len(results)
    passed = len([r for r in results if r["status"] == "PASS"])
    
    report_content = f"""# Validation Report: Stage 1 Digital FTE (RevOps)

## Summary
- **Total Leads Processed:** {total}
- **Passed:** {passed}
- **Failed:** {total - passed}
- **Accuracy:** {(passed/total)*100:.2f}%

## Detailed Results
"""
    for r in results:
        report_content += f"### {r['lead']}\n"
        report_content += f"- **Status:** {r['status']}\n"
        report_content += f"- **Score:** {r['actual']['score']}\n"
        report_content += f"- **Action:** {r['actual']['action']}\n"
        if r['errors']:
            report_content += f"- **Errors:** {', '.join(r['errors'])}\n"
        report_content += f"- **Reasoning:** {r['actual']['reasoning']}\n\n"

    with open("specs/revops-fte/stage-1-validation-report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"-------------------------------------------------------")
    print(f"📊 Validation Complete. Report generated: specs/revops-fte/stage-1-validation-report.md")

if __name__ == "__main__":
    results = asyncio.run(run_validation_sprint())
    generate_report(results)
