import platform
import datetime
from fastapi import FastAPI, HTTPException

app = FastAPI(title="SentinelCloud API", version="1.0.0")

class InfrastructureAuditor:
    """
    Business logic for system health and security auditing.
    Modular design to allow for future Cloud (AWS/Azure) integration.
    """
    def __init__(self):
        self.system_info = platform.uname()

    def perform_security_check(self):
        # In a real scenario, this would check for open ports or MFA status
        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "os": self.system_info.system,
            "node": self.system_info.node,
            "status": "SECURE",
            "mfa_policy_check": "COMPLIANT",
            "unauthorized_access_attempts": 0
        }

@app.get("/")
async def root():
    return {"message": "SentinelCloud API is operational. System monitoring active."}

@app.get("/audit/health")
async def get_health():
    """Endpoint to check infrastructure reliability."""
    try:
        auditor = InfrastructureAuditor()
        return auditor.perform_security_check()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run this: pip install fastapi uvicorn
# Command: uvicorn sentinel_api:app --reload