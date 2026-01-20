# AWS Personal Cloud

A serverless personal cloud storage solution built with AWS and Terraform.

## Features
- **Raw Uploads Bucket**: Files uploaded here are automatically moved to Glacier after 30 days.
- **Processed Bucket**: Standard storage for processed files.
- **Least Privilege Access**: Dedicated IAM user and policy for secure access.

## Prerequisites
- Terraform
- AWS CLI
- Python 3.x

## Setup

1. Clone the repository.
2. Create a `.env` file with your AWS credentials:
   ```
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_REGION=us-east-1
   ```
3. Initialize Terraform:
   ```bash
   cd infrastructure
   terraform init
   terraform apply
   ```

## Usage
Use the `upload_test.py` script to verify uploads:
```bash
python scripts/upload_test.py <bucket_name>
```
