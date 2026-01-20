output "raw_bucket_name" {
  description = "Name of the raw uploads bucket"
  value       = aws_s3_bucket.raw_bucket.bucket
}

output "processed_bucket_name" {
  description = "Name of the processed storage bucket"
  value       = aws_s3_bucket.processed_bucket.bucket
}

output "iam_policy_arn" {
  description = "ARN of the created IAM policy"
  value       = aws_iam_policy.personal_cloud_policy.arn
}
