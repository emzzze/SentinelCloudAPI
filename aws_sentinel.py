from dotenv import load_dotenv
load_dotenv()

import os
import boto3
from typing import List, Dict
from datetime import datetime

class AWSSentinel:
    """
    AWS Security Auditor for S3 bucket compliance scanning.
    Checks for public access, encryption, versioning, and logging.
    """
    
    def __init__(self):
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        
        if not self.aws_access_key or not self.aws_secret_key:
            raise ValueError("AWS credentials not found in environment")
        
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.aws_region
        )
    
    def list_buckets(self) -> List[str]:
        """List all S3 buckets in the account."""
        response = self.s3_client.list_buckets()
        return [bucket['Name'] for bucket in response['Buckets']]
    
    def check_bucket_public_access(self, bucket_name: str) -> Dict:
        """Check if bucket allows public access."""
        try:
            acl = self.s3_client.get_bucket_acl(Bucket=bucket_name)
            
            public_read = False
            public_write = False
            
            for grant in acl['Grants']:
                grantee = grant.get('Grantee', {})
                permission = grant.get('Permission')
                
                # Check for public access
                if grantee.get('Type') == 'Group' and 'AllUsers' in grantee.get('URI', ''):
                    if permission == 'READ':
                        public_read = True
                    if permission in ['WRITE', 'FULL_CONTROL']:
                        public_write = True
            
            return {
                "bucket": bucket_name,
                "public_read": public_read,
                "public_write": public_write,
                "status": "CRITICAL" if public_write else ("WARNING" if public_read else "SECURE")
            }
        except Exception as e:
            return {
                "bucket": bucket_name,
                "error": str(e),
                "status": "ERROR"
            }
    
    def check_bucket_encryption(self, bucket_name: str) -> Dict:
        """Check if bucket has encryption enabled."""
        try:
            encryption = self.s3_client.get_bucket_encryption(Bucket=bucket_name)
            return {
                "bucket": bucket_name,
                "encryption_enabled": True,
                "rules": encryption.get('Rules', []),
                "status": "SECURE"
            }
        except self.s3_client.exceptions.ServerSideEncryptionConfigurationNotFoundError:
            return {
                "bucket": bucket_name,
                "encryption_enabled": False,
                "status": "WARNING"
            }
        except Exception as e:
            return {
                "bucket": bucket_name,
                "error": str(e),
                "status": "ERROR"
            }
    
    def check_bucket_versioning(self, bucket_name: str) -> Dict:
        """Check if bucket has versioning enabled."""
        try:
            versioning = self.s3_client.get_bucket_versioning(Bucket=bucket_name)
            status = versioning.get('Status', 'Disabled')
            
            return {
                "bucket": bucket_name,
                "versioning_enabled": status == 'Enabled',
                "status": "SECURE" if status == 'Enabled' else "INFO"
            }
        except Exception as e:
            return {
                "bucket": bucket_name,
                "error": str(e),
                "status": "ERROR"
            }
    
    def full_security_audit(self, bucket_name: str) -> Dict:
        """Perform complete security audit on a bucket."""
        return {
            "bucket": bucket_name,
            "timestamp": datetime.utcnow().isoformat(),
            "public_access": self.check_bucket_public_access(bucket_name),
            "encryption": self.check_bucket_encryption(bucket_name),
            "versioning": self.check_bucket_versioning(bucket_name)
        }
    
    def audit_all_buckets(self) -> List[Dict]:
        """Audit all S3 buckets in the account."""
        buckets = self.list_buckets()
        results = []
        
        for bucket in buckets:
            audit = self.full_security_audit(bucket)
            results.append(audit)
        
        return results


if __name__ == "__main__":
    # Test the AWS Sentinel
    try:
        sentinel = AWSSentinel()
        print("AWS Sentinel initialized successfully")
        print(f"Region: {sentinel.aws_region}")
        
        print("\nListing S3 buckets...")
        buckets = sentinel.list_buckets()
        print(f"Found {len(buckets)} buckets: {buckets}")
        
        if buckets:
            print(f"\nAuditing first bucket: {buckets[0]}")
            audit = sentinel.full_security_audit(buckets[0])
            print(audit)
    except ValueError as e:
        print(f"ERROR: {e}")
        print("Add AWS credentials to .env file")
