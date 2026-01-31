from dotenv import load_dotenv
load_dotenv()

import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY not found in environment")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ShadowGate:
    """
    JWT-based authentication system for Sentinel API.
    Handles token generation, validation, and password hashing.
    """
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for secure storage."""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token.
        
        Args:
            data: Payload to encode in the token (e.g., {"sub": "username"})
            expires_delta: Token expiration time
        
        Returns:
            Encoded JWT token string
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token string
        
        Returns:
            Decoded token payload
        
        Raises:
            JWTError: If token is invalid or expired
        """
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except JWTError as e:
            raise ValueError(f"Invalid token: {e}")


if __name__ == "__main__":
    # Test the gate
    gate = ShadowGate()
    
    # Test password hashing
    password = "SentinelAdmin2026!"
    hashed = gate.hash_password(password)
    print(f"Password: {password}")
    print(f"Hashed: {hashed}")
    print(f"Verification: {gate.verify_password(password, hashed)}")
    print(f"Wrong password: {gate.verify_password('wrong', hashed)}")
    
    print("\n" + "=" * 60)
    
    # Test token creation
    token = gate.create_access_token({"sub": "admin", "role": "superuser"})
    print(f"Generated Token: {token}")
    
    # Test token verification
    decoded = gate.verify_token(token)
    print(f"Decoded Token: {decoded}")
    
    print("\n" + "=" * 60)
    print("Shadow-Gate operational. Authentication system ready.")
