#!/bin/bash
BUCKET_NAME="sentinel-test-$(date +%s)"
aws s3 mb s3://$BUCKET_NAME --region us-east-1
echo "Created bucket: $BUCKET_NAME"
