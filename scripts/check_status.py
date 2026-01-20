import boto3
import os

def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key.strip()] = value.strip()

def check_resources():
    load_env()
    s3 = boto3.client('s3')
    iam = boto3.client('iam')
    
    print("Checking Buckets:")
    try:
        response = s3.list_buckets()
        for b in response['Buckets']:
            if 'cloud-uploads-raw' in b['Name'] or 'cloud-storage-processed' in b['Name']:
                print(f" - Found Bucket: {b['Name']}")
    except Exception as e:
        print(f"Error listing buckets: {e}")

    print("\nChecking Policies:")
    try:
        # List policies (local scope first)
        response = iam.list_policies(Scope='Local')
        for p in response['Policies']:
            if 'PersonalCloudS3Access' in p['PolicyName']:
                print(f" - Found Policy: {p['PolicyName']} (ARN: {p['Arn']})")
    except Exception as e:
        print(f"Error listing policies: {e}")

if __name__ == "__main__":
    check_resources()
