resource "aws_iam_role" "lambda_role" {
  name = "${var.tags["name"]}_lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
  tags = {
    Name = "${var.tags["name"]}_s3_cleaner"
  }
}


resource "aws_iam_policy" "s3cleaner" {
  name        = "${var.tags["name"]}_S3CleanupPolicy"
  description = "Policy that allows Lambda to delete S3 objects and buckets"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:ListAllMyBuckets",
        "s3:GetBucketLocation",
        "s3:ListBucket",
        "s3:ListBucketVersions",
        "s3:DeleteObject",
        "s3:DeleteObjectVersion",
        "s3:DeleteBucket"
      ]
      Resource = "*"
    }]
  })
  tags = {
    Name = "${var.tags["name"]}_s3_cleaner"
  }
}

resource "aws_iam_policy_attachment" "lambda_s3cleaner" {
  name       = "lambda_s3cleaner"
  roles      = [aws_iam_role.lambda_role.name]
  policy_arn = aws_iam_policy.s3cleaner.arn
}
