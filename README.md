# SentinelCloud-API 

A lightweight, modular backend service built with **Python (FastAPI)** designed to monitor system health and audit security configurations in real-time.

##  Features
- **Backend Services:** Designed with Python for high performance and readability.
- **Infrastructure Auditing:** Built-in logic to verify OS security and system reliability.
- **Clean Code:** Follows modular OOP (Object-Oriented Programming) principles.
- **Auto-Documentation:** Built-in Swagger UI (FastAPI) for API testing.

##  Architecture
The service is structured to separate business logic (Auditor) from the API routing (Endpoints). This ensures the code is **testable** and **scalable**, allowing for future integrations with Cloud providers like AWS or Azure.

##  Getting Started
1. Clone the repo: `git clone https://github.com/YOUR_USERNAME/SentinelCloud-API.git`
2. Install dependencies: `pip install fastapi uvicorn`
3. Run the server: `uvicorn sentinel_api:app --reload`
4. Access the API documentation at: `http://127.0.0.1:8000/docs`

##  Future Roadmap
- Integration with AWS Boto3 for real-time S3 bucket security auditing.
- Containerization using **Docker**.
- Implementation of **Nix** for reproducible dev environments (inspired by MixRank's tech stack).
