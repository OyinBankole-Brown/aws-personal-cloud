import boto3
import os
from botocore.exceptions import ClientError, NoCredentialsError

def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key.strip()] = value.strip()
    else:
        print(".env file not found")

def verify():
    load_env()
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print("SUCCESS: Credentials are valid.")
        print(f"Account: {identity['Account']}")
        print(f"ARN: {identity['Arn']}")
    except NoCredentialsError:
        print("FAILURE: No credentials found.")
    except ClientError as e:
        print(f"FAILURE: {e}")
    except Exception as e:
        print(f"FAILURE: Unexpected error: {e}")

if __name__ == "__main__":
    verify()
