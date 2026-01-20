terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Unique suffix to ensure bucket uniqueness
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# 1. Cloud Uploads Raw Bucket
resource "aws_s3_bucket" "raw_bucket" {
  bucket = "cloud-uploads-raw-${random_id.bucket_suffix.hex}"
}

# Lifecycle Policy for Raw Bucket (Move to Glacier after 30 days)
resource "aws_s3_bucket_lifecycle_configuration" "raw_bucket_lifecycle" {
  bucket = aws_s3_bucket.raw_bucket.id

  rule {
    id     = "MoveToGlacier"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "GLACIER"
    }
    
    # Lifecycle Policy: Transition to Glacier after 30 days
  }
}

# 2. Cloud Storage Processed Bucket
resource "aws_s3_bucket" "processed_bucket" {
  bucket = "cloud-storage-processed-${random_id.bucket_suffix.hex}"
}

# 3. IAM Policy for Least Privilege Access
resource "aws_iam_policy" "personal_cloud_policy" {
  name        = "PersonalCloudS3Access"
  description = "Least privilege access to personal cloud raw and processed buckets"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "ListBuckets"
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.raw_bucket.arn,
          aws_s3_bucket.processed_bucket.arn
        ]
      },
      {
        Sid    = "ObjectAccess"
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject"
        ]
        Resource = [
          "${aws_s3_bucket.raw_bucket.arn}/*",
          "${aws_s3_bucket.processed_bucket.arn}/*"
        ]
      }
    ]
  })
}
