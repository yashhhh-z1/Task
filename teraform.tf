provider "aws" {
  region = "ap-south-1"
}

resource "aws_ecr_repository" "repo" {
  name = "task_ecr"
}
resource "aws_lambda_function" "s3_to_rds_or_glue" {
  function_name = "s3_to_rds_or_glue"
  package_type  = "Image"
  image_uri     = "admin.dkr.ecr.your-region.amazonaws.com/my-repo:latest"
  role          = aws_iam_role.lambda_exec.arn
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
