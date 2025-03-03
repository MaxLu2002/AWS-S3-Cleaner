data "archive_file" "lambda_package" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "my_lambda" {
  function_name    = "${var.tags["name"]}_s3_cleaner"
  role             = aws_iam_role.lambda_role.arn
  handler          = "main.lambda_handler"
  runtime          = "python3.9"
  filename         = data.archive_file.lambda_package.output_path
  source_code_hash = data.archive_file.lambda_package.output_base64sha256
  timeout          = 900
  memory_size      = 128

  tags = {
    Name = "${var.tags["name"]}_s3_cleaner"
  }
}
