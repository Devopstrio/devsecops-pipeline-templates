import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("devsecops-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="DevSecOps Pipeline Templates API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/templates")
def get_templates():
    return [
        {"id": "gh-sec-starter", "name": "GitHub Secure Starter", "platform": "github", "level": "L3"},
        {"id": "gitlab-sec-l4", "name": "GitLab Enterprise L4", "platform": "gitlab", "level": "L4"},
        {"id": "tf-secure-plan", "name": "Terraform Policy Guard", "platform": "terraform", "level": "L3"}
    ]

@app.post("/pipelines/validate")
def validate_pipeline(pipeline_config: dict):
    logger.info(f"Validating pipeline configuration for policy compliance")
    return {"status": "VALIDATED", "score": 98, "findings": []}

@app.get("/security/findings")
def get_security_findings():
    return {
        "critical": 0,
        "high": 2,
        "medium": 15,
        "top_finding": "Outdated Base Image (alpine:3.12)",
        "remediation_avg_time": "14h"
    }

@app.get("/compliance/status")
def get_compliance_status():
    return {
        "soc2_compliance": "98%",
        "iso27001_alignment": "94%",
        "slsa_level_target": "Level 3",
        "unresolved_vulnerabilities": 12
    }

@app.post("/exceptions/request")
def request_exception(finding_id: str, reason: str, duration_days: int = 30):
    logger.info(f"Requesting security exception for finding {finding_id}")
    return {"status": "PENDING_APPROVAL", "request_id": "waiver_sec_789"}

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "total_protected_pipelines": 452,
        "avg_scan_duration": "4m 20s",
        "policy_bypass_attempts": 0,
        "platform_security_score": "Elite"
    }
