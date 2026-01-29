from dotenv import load_dotenv
load_dotenv()  # This loads .env file


import os
from cryptography.fernet import Fernet

class SecurityVault:
    """
    Sentinel-Vault: A modular encryption service for 
    handling sensitive system credentials.
    """
    def __init__(self, master_key: str = None):
        # Load from env if not provided
        self.key = master_key or os.getenv("SENTINEL_MASTER_KEY")
        
        if not self.key:
            raise ValueError("SENTINEL_MASTER_KEY not found in environment")
        
        # Ensure key is bytes (Fernet requires bytes, not string)
        if isinstance(self.key, str):
            self.key = self.key.encode()
            
        self.cipher = Fernet(self.key)
    
    def encrypt_secret(self, secret_text: str):
        """Encrypts a string using AES-256."""
        try:
            return self.cipher.encrypt(secret_text.encode()).decode()
        except Exception as e:
            raise ValueError(f"Encryption failed: {e}")
    
    def decrypt_secret(self, encrypted_text: str):
        """Decrypts a string back to plain text."""
        try:
            return self.cipher.decrypt(encrypted_text.encode()).decode()
        except Exception as e:
            raise ValueError(f"Decryption failed. Invalid key or corrupted data: {e}")


def generate_master_key():
    """Generate a new master key. Save this to your .env file."""
    key = Fernet.generate_key().decode()
    print("=" * 60)
    print("NEW MASTER KEY GENERATED")
    print("=" * 60)
    print(f"SENTINEL_MASTER_KEY={key}")
    print("=" * 60)
    print("WARNING: Save this to your .env file immediately")
    print("WARNING: Do not commit this to version control")
    print("=" * 60)
    return key


if __name__ == "__main__":
    # Uncomment this line to generate a new master key
    #generate_master_key()
    
    # Normal usage (requires SENTINEL_MASTER_KEY in environment)
    try:
        vault = SecurityVault()
        test_secret = "SentinelCloud_Admin_Pass_2026"
        
        locked = vault.encrypt_secret(test_secret)
        print(f"ENCRYPTED: {locked}")
        
        unlocked = vault.decrypt_secret(locked)
        print(f"DECRYPTED: {unlocked}")
        
    except ValueError as e:
        print(f"ERROR: {e}")
        print("TIP: Run generate_master_key() first and add it to .env")
