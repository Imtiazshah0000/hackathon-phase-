from prometheus_client import Counter, Histogram, Summary, start_http_server
from typing import Optional

# 1. Lead Processing Throughput & Status (ADR-4)
LEADS_PROCESSED = Counter("revops_leads_total", "Total leads processed", ["status"])
AUTONOMOUS_OUTREACH = Counter("revops_outreach_total", "Total autonomous outreach sent", ["channel"])
ESCALATIONS = Counter("revops_escalations_total", "Total human-in-the-loop triggers")

# 2. Performance & Latency
LEAD_PROCESSING_TIME = Histogram("revops_lead_processing_seconds", "Time spent processing a single lead")

# 3. Cost Control (Token Usage)
TOKEN_CONSUMPTION = Counter("revops_tokens_total", "Total OpenAI token usage", ["model", "type"]) # type: prompt/completion

# 4. Error Rates
PROCESSING_ERRORS = Counter("revops_errors_total", "Total lead processing errors", ["error_type"])

def start_metrics_server(port: int = 9000):
    """Starts a dedicated Prometheus metrics server."""
    print(f"Prometheus metrics available on port {port}")
    start_http_server(port)

def track_token_usage(model: str, prompt: int, completion: int):
    """Updates the token consumption metric."""
    TOKEN_CONSUMPTION.labels(model=model, type="prompt").inc(prompt)
    TOKEN_CONSUMPTION.labels(model=model, type="completion").inc(completion)
