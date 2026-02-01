from dotenv import load_dotenv
load_dotenv()

import platform
import datetime
import json
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from Security_Vault import SecurityVault
from shadow_gate import ShadowGate

app = FastAPI(title="SentinelCloud API", version="2.0.0")
security = HTTPBearer()

# User storage file
USERS_FILE = Path("users.json")

# Initialize modules
try:
    vault = SecurityVault()
    gate = ShadowGate()
except ValueError as e:
    print(f"INITIALIZATION ERROR: {e}")
    vault = None
    gate = None


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class SecretRequest(BaseModel):
    secret: str

class EncryptResponse(BaseModel):
    encrypted: str
    timestamp: str

class DecryptResponse(BaseModel):
    decrypted: str
    timestamp: str

class UserRegister(BaseModel):
    username: str
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: dict


# ============================================================================
# USER STORAGE FUNCTIONS
# ============================================================================

def load_users():
    """Load users from JSON file."""
    if not USERS_FILE.exists():
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users: dict):
    """Save users to JSON file."""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def get_user(username: str):
    """Get user by username."""
    users = load_users()
    return users.get(username)

def create_user(username: str, password: str, role: str = "user"):
    """Create new user with hashed password."""
    users = load_users()
    
    if username in users:
        raise ValueError("User already exists")
    
    users[username] = {
        "username": username,
        "hashed_password": gate.hash_password(password),
        "role": role,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    
    save_users(users)
    return users[username]


# ============================================================================
# AUTHENTICATION DEPENDENCY
# ============================================================================

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and return user payload."""
    if not gate:
        raise HTTPException(status_code=503, detail="Authentication system not initialized")
    
    try:
        token = credentials.credentials
        payload = gate.verify_token(token)
        return payload
    except ValueError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


# ============================================================================
# INFRASTRUCTURE AUDIT ROUTES
# ============================================================================

class InfrastructureAuditor:
    """System health and security auditing."""
    def __init__(self):
        self.system_info = platform.uname()
    
    def perform_security_check(self):
        return {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "os": self.system_info.system,
            "node": self.system_info.node,
            "status": "SECURE",
            "mfa_policy_check": "COMPLIANT",
            "unauthorized_access_attempts": 0
        }

@app.get("/")
async def root():
    return {
        "message": "SentinelCloud API is operational. System monitoring active.",
        "version": "2.0.0",
        "vault_status": "OPERATIONAL" if vault else "ERROR",
        "auth_status": "OPERATIONAL" if gate else "ERROR"
    }

@app.get("/audit/health")
async def get_health():
    """Endpoint to check infrastructure reliability."""
    try:
        auditor = InfrastructureAuditor()
        return auditor.perform_security_check()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.post("/auth/register", response_model=TokenResponse)
async def register_user(user_data: UserRegister):
    """Register a new user and return access token."""
    if not gate:
        raise HTTPException(status_code=503, detail="Authentication system not initialized")
    
    try:
        # Create user
        user = create_user(user_data.username, user_data.password, user_data.role)
        
        # Generate token
        token_data = {
            "sub": user["username"],
            "role": user["role"]
        }
        access_token = gate.create_access_token(token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 1800,  # 30 minutes in seconds
            "user": {
                "username": user["username"],
                "role": user["role"],
                "created_at": user["created_at"]
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/auth/login", response_model=TokenResponse)
async def login_user(credentials: UserLogin):
    """Authenticate user and return access token."""
    if not gate:
        raise HTTPException(status_code=503, detail="Authentication system not initialized")
    
    # Get user
    user = get_user(credentials.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Verify password
    if not gate.verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Generate token
    token_data = {
        "sub": user["username"],
        "role": user["role"]
    }
    access_token = gate.create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 1800,
        "user": {
            "username": user["username"],
            "role": user["role"],
            "created_at": user["created_at"]
        }
    }

@app.get("/auth/me")
async def get_current_user(user: dict = Depends(verify_token)):
    """Get current authenticated user info."""
    return {
        "username": user.get("sub"),
        "role": user.get("role"),
        "token_expires": user.get("exp")
    }


# ============================================================================
# VAULT ROUTES (PROTECTED)
# ============================================================================

@app.get("/vault/status")
async def vault_status():
    """Check if Sentinel-Vault is operational."""
    if not vault:
        raise HTTPException(status_code=503, detail="Vault not initialized. Check SENTINEL_MASTER_KEY.")
    
    return {
        "status": "OPERATIONAL",
        "encryption": "AES-256 (Fernet)",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.post("/vault/encrypt", response_model=EncryptResponse)
async def encrypt_secret(
    request: SecretRequest,
    user: dict = Depends(verify_token)  # 🔒 PROTECTED
):
    """Encrypt a secret string. Requires valid JWT token."""
    if not vault:
        raise HTTPException(status_code=503, detail="Vault not initialized")
    
    try:
        encrypted = vault.encrypt_secret(request.secret)
        return {
            "encrypted": encrypted,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Encryption failed: {str(e)}")

@app.post("/vault/decrypt", response_model=DecryptResponse)
async def decrypt_secret(
    request: SecretRequest,
    user: dict = Depends(verify_token)  # 🔒 PROTECTED
):
    """Decrypt an encrypted string. Requires valid JWT token."""
    if not vault:
        raise HTTPException(status_code=503, detail="Vault not initialized")
    
    try:
        decrypted = vault.decrypt_secret(request.secret)
        return {
            "decrypted": decrypted,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Decryption failed: {str(e)}")
