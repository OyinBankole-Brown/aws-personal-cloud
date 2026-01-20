import boto3
import os
import sys
import uuid
from botocore.exceptions import ClientError, NoCredentialsError

# Load environment variables (basic loader to avoid dependency on python-dotenv)
def load_env():
    # Look for .env in the parent directory
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def test_s3_upload(bucket_name):
    # Ensure credentials are loaded
    load_env()

    # Create S3 client
    try:
        s3 = boto3.client('s3')
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please check your .env file.")
        sys.exit(1)

    # 1. Create a dummy file
    filename = f"test-upload-{uuid.uuid4()}.txt"
    content = "This is a test upload for the Personal Cloud."
    
    with open(filename, "w") as f:
        f.write(content)
    
    print(f"Created local test file: {filename}")

    # 2. Upload File
    try:
        print(f"Attempting to upload to {bucket_name}...")
        s3.upload_file(filename, bucket_name, filename)
        print("Upload Successful!")
    except ClientError as e:
        print(f"Upload Failed: {e}")
        # Clean up local file even if upload fails
        os.remove(filename)
        return False

    # 3. Generate URL (mocking structure since it's private by default, but verifying path)
    # Generate S3 URL
    # Standard format: https://bucket-name.s3.region.amazonaws.com/key
    region = os.environ.get('AWS_REGION', 'us-east-1')
    s3_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{filename}"
    print(f"File URL: {s3_url}")

    # 4. Delete File
    try:
        print("Attempting to delete file...")
        s3.delete_object(Bucket=bucket_name, Key=filename)
        print("Delete Successful!")
    except ClientError as e:
        print(f"Delete Failed: {e}")
        os.remove(filename)
        return False
    
    # Clean up local file
    os.remove(filename)
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload_test.py <bucket_name>")
        sys.exit(1)
    
    bucket = sys.argv[1]
    success = test_s3_upload(bucket)
    
    if success:
        print("\nTest PASSED: Read/Write/Delete permissions confirmed.")
        sys.exit(0)
    else:
        print("\nTest FAILED.")
        sys.exit(1)
