# Sentinel Cloud API

**Enterprise-grade security infrastructure for credential management and authentication.**

Sentinel Cloud API is a modular Python-based security system combining AES-256 encryption, JWT authentication, and infrastructure monitoring. Built for developers who need production-ready secret management without the overhead of complex cloud solutions.

---

## Architecture Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                      SENTINEL CLOUD API                          │
│                       (sentinel_api.py)                          │
│                     FastAPI + Uvicorn Server                     │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼────────────────────┐
          │                   │                    │
          ▼                   ▼                    ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   AUDIT MODULE   │  │  VAULT MODULE    │  │  AUTH MODULE     │
│   /audit/*       │  │  /vault/*        │  │  /auth/*         │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│ • Health Check   │  │ • Encrypt        │  │ • Login          │
│ • Security Scan  │  │ • Decrypt        │  │ • Register       │
│ • System Status  │  │ • Status         │  │ • Protected      │
└──────────────────┘  └──────────────────┘  └──────────────────┘
                              │                    │
                              ▼                    ▼
                      ┌──────────────┐    ┌──────────────┐
                      │ SENTINEL-    │    │ SHADOW-      │
                      │ VAULT        │    │ GATE         │
                      ├──────────────┤    ├──────────────┤
                      │ AES-256      │    │ JWT Tokens   │
                      │ Fernet       │    │ bcrypt Hash  │
                      │ Encryption   │    │ Auth Logic   │
                      └──────────────┘    └──────────────┘
                              │                    │
                              └────────┬───────────┘
                                       ▼
                              ┌─────────────────┐
                              │  ENVIRONMENT    │
                              │    (.env)       │
                              ├─────────────────┤
                              │ Master Keys     │
                              │ JWT Secrets     │
                              │ API Tokens      │
                              └─────────────────┘
```

---

## Features

### 🔐 **Sentinel-Vault (Encryption Module)**
- **AES-256 symmetric encryption** using Fernet
- Secure credential storage for API keys, passwords, database credentials
- Master key-based access control
- Industry-standard cryptography (`cryptography` library by pyca)

### 🛡️ **Shadow-Gate (Authentication Module)**
- **JWT (JSON Web Tokens)** for stateless authentication
- **bcrypt password hashing** (never store plain-text passwords)
- Token expiration and validation
- Role-based access control ready

### 📊 **Infrastructure Auditor**
- System health monitoring
- Security compliance checks
- Real-time infrastructure status reporting

---

## Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment support

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/SentinelCloudAPI.git
cd SentinelCloudAPI

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

1. **Generate Master Keys:**
```bash
# Generate Vault Master Key
python3 -c "from cryptography.fernet import Fernet; print(f'SENTINEL_MASTER_KEY={Fernet.generate_key().decode()}')"

# Generate JWT Secret Key
python3 -c "import secrets; print(f'JWT_SECRET_KEY={secrets.token_urlsafe(32)}')"
```

2. **Create `.env` file:**
```bash
touch .env
nano .env
```

3. **Add your keys to `.env`:**
```
SENTINEL_MASTER_KEY=your_generated_vault_key_here
JWT_SECRET_KEY=your_generated_jwt_key_here
```

⚠️ **CRITICAL:** Never commit `.env` to version control. It's already in `.gitignore`.

---

## Running the API
```bash
# Activate virtual environment
source venv/bin/activate

# Start the server
uvicorn sentinel_api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Server:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

---

## API Endpoints

### Infrastructure Audit
```http
GET /                    # API health check
GET /audit/health        # System security status
```

### Vault (Encryption)
```http
GET  /vault/status       # Check encryption operational status
POST /vault/encrypt      # Encrypt a secret
POST /vault/decrypt      # Decrypt an encrypted secret
```

**Example - Encrypt a Secret:**
```bash
curl -X POST http://localhost:8000/vault/encrypt \
  -H "Content-Type: application/json" \
  -d '{"secret":"MyDatabasePassword_2026"}'
```

**Response:**
```json
{
  "encrypted": "gAAAAABl...",
  "timestamp": "2026-01-30T12:34:56"
}
```

### Authentication (Coming Soon)
```http
POST /auth/register      # Create new user
POST /auth/login         # Get JWT token
GET  /auth/protected     # Access protected resource
```

---

## Project Structure
```
SentinelCloudAPI/
├── .env                    # Environment variables (NOT committed)
├── .gitignore              # Git exclusions
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── sentinel_api.py         # Main FastAPI application
├── Security_Vault.py       # Encryption module (Sentinel-Vault)
├── shadow_gate.py          # Authentication module (Shadow-Gate)
└── venv/                   # Virtual environment (NOT committed)
```

---

## Security Architecture

### Encryption Flow
1. User submits plaintext secret to `/vault/encrypt`
2. Sentinel-Vault encrypts using AES-256 with Master Key
3. Returns base64-encoded ciphertext
4. Only requests with valid Master Key can decrypt

### Authentication Flow (In Progress)
1. User registers → Shadow-Gate hashes password with bcrypt
2. User logs in → Shadow-Gate verifies password, issues JWT
3. User accesses protected route → API validates JWT signature
4. If valid → Access granted with user context

### Defense Layers
- **Layer 1:** JWT Authentication (identity verification)
- **Layer 2:** AES-256 Encryption (data protection at rest)
- **Layer 3:** Environment Variables (secret key isolation)
- **Layer 4:** Git Security (`.gitignore` prevents credential leaks)

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Web Framework** | FastAPI | High-performance async API |
| **Server** | Uvicorn | ASGI server for FastAPI |
| **Encryption** | Fernet (AES-256) | Symmetric encryption |
| **JWT Handling** | python-jose | Token generation/validation |
| **Password Hashing** | passlib + bcrypt | Secure password storage |
| **Environment** | python-dotenv | Secret management |

---

## Development Roadmap

### ✅ Phase 1: Core Security Infrastructure (Complete)
- [x] Sentinel-Vault (AES-256 Encryption Module)
- [x] Shadow-Gate (JWT Authentication Module)
- [x] Basic API Infrastructure with FastAPI
- [x] Environment-based Secret Management

### 🔄 Phase 2: Authentication & Access Control (In Progress)
- [ ] User Registration & Login Endpoints
- [ ] User Storage (JSON → SQLite → PostgreSQL migration path)
- [ ] JWT Route Protection Middleware
- [ ] Role-Based Access Control (RBAC)
- [ ] API Key Management System

### 📋 Phase 3: Cloud Integration
- [ ] AWS Boto3 Integration for S3 bucket security auditing
- [ ] Real-time cloud resource monitoring
- [ ] Automated compliance scanning
- [ ] Multi-cloud support (AWS, Azure, GCP)

### 🐳 Phase 4: Containerization & Deployment
- [ ] Docker containerization
- [ ] Docker Compose for local development
- [ ] Kubernetes deployment configurations
- [ ] CI/CD pipeline (GitHub Actions)

### 🔧 Phase 5: Developer Experience
- [ ] Nix-based reproducible development environments (inspired by MixRank)
- [ ] Development environment automation
- [ ] One-command setup for new developers
- [ ] Deterministic builds across platforms

### 🚀 Phase 6: Production Hardening
- [ ] Rate limiting and DDoS protection
- [ ] Audit logging and SIEM integration
- [ ] Automated security scanning
- [ ] High-availability configuration
- [ ] Production deployment guide

### 📊 Phase 7: Monitoring & Analytics
- [ ] Prometheus metrics integration
- [ ] Grafana dashboards
- [ ] Alert system for security events
- [ ] Performance monitoring

## Testing

### Test Encryption Module
```bash
python Security_Vault.py
```

### Test Authentication Module
```bash
python shadow_gate.py
```

### Interactive API Testing
Visit http://localhost:8000/docs for Swagger UI testing interface.

---

## Security Best Practices

✅ **Never commit `.env` files**  
✅ **Rotate keys periodically**  
✅ **Use HTTPS in production**  
✅ **Implement rate limiting on auth endpoints**  
✅ **Monitor for suspicious activity**  
✅ **Keep dependencies updated**  

---

## Contributing

This is a personal infrastructure project. If you're building something similar:
1. Fork the repository
2. Implement your security layer
3. Never share your `.env` file
4. Test thoroughly before production

---

## License

MIT License - Use at your own risk. This is infrastructure code; security is your responsibility.

---

## Author

**Built by emzzze for AlphaGuardIT**  
Architect of the Mainframe | Cyber-Technical Infrastructure  
Montreal → Washington

---

## Acknowledgments

- Cryptography by [pyca](https://cryptography.io/)
- FastAPI by [Sebastián Ramírez](https://fastapi.tiangolo.com/)
- Authentication patterns inspired by enterprise security standards

---

**Status:** 🟢 Operational | Shadow-Gate Active | Vault Secured
