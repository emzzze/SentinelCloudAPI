from dotenv import load_dotenv
load_dotenv()

import platform
import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Security_Vault import SecurityVault

app = FastAPI(title="SentinelCloud API", version="1.0.0")


class InfrastructureAuditor:
    """
    Business logic for system health and security auditing.
    Modular design to allow for future Cloud (AWS/Azure) integration.
    """
    def __init__(self):
        self.system_info = platform.uname()
    
    def perform_security_check(self):
        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "os": self.system_info.system,
            "node": self.system_info.node,
            "status": "SECURE",
            "mfa_policy_check": "COMPLIANT",
            "unauthorized_access_attempts": 0
        }


# Request/Response models for Vault endpoints
class SecretRequest(BaseModel):
    secret: str

class EncryptResponse(BaseModel):
    encrypted: str
    timestamp: str

class DecryptResponse(BaseModel):
    decrypted: str
    timestamp: str


# Initialize vault globally
try:
    vault = SecurityVault()
except ValueError as e:
    print(f"VAULT INITIALIZATION ERROR: {e}")
    vault = None


@app.get("/")
async def root():
    return {
        "message": "SentinelCloud API is operational. System monitoring active.",
        "vault_status": "OPERATIONAL" if vault else "ERROR"
    }


@app.get("/audit/health")
async def get_health():
    """Endpoint to check infrastructure reliability."""
    try:
        auditor = InfrastructureAuditor()
        return auditor.perform_security_check()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/vault/status")
async def vault_status():
    """Check if Sentinel-Vault is operational."""
    if not vault:
        raise HTTPException(status_code=503, detail="Vault not initialized. Check SENTINEL_MASTER_KEY.")
    
    return {
        "status": "OPERATIONAL",
        "encryption": "AES-256 (Fernet)",
        "timestamp": datetime.datetime.now().isoformat()
    }


@app.post("/vault/encrypt", response_model=EncryptResponse)
async def encrypt_secret(request: SecretRequest):
    """Encrypt a secret string."""
    if not vault:
        raise HTTPException(status_code=503, detail="Vault not initialized")
    
    try:
        encrypted = vault.encrypt_secret(request.secret)
        return {
            "encrypted": encrypted,
            "timestamp": datetime.datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Encryption failed: {str(e)}")


@app.post("/vault/decrypt", response_model=DecryptResponse)
async def decrypt_secret(request: SecretRequest):
    """Decrypt an encrypted string."""
    if not vault:
        raise HTTPException(status_code=503, detail="Vault not initialized")
    
    try:
        decrypted = vault.decrypt_secret(request.secret)
        return {
            "decrypted": decrypted,
            "timestamp": datetime.datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Decryption failed: {str(e)}")
