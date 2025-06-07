provider "aws" {
  region  = "us-east-1"
}

# Crear el bucket principal
resource "aws_s3_bucket" "data_analyst_demo_roly" {
  bucket = "data-analyst-demo-roly"
  force_destroy = true
}

# Crear los "folders" (prefixes) input/, output/ y lambda-terraform-state/
resource "aws_s3_object" "input_folder" {
  bucket = aws_s3_bucket.data_analyst_demo_roly.id
  key    = "input/"
}

resource "aws_s3_object" "output_folder" {
  bucket = aws_s3_bucket.data_analyst_demo_roly.id
  key    = "output/"
}

resource "aws_s3_object" "lambda_terraform_state_folder" {
  bucket = aws_s3_bucket.data_analyst_demo_roly.id
  key    = "lambda-terraform-state/"
}

resource "aws_s3_object" "input_sales_csv" {
  bucket = aws_s3_bucket.data_analyst_demo_roly.id
  key    = "input/sales.csv"
  content = <<CSV
region,sales
Norte,100
Sur,200
Norte,150
Este,300
Sur,100
Oeste,250
Este,200
CSV
  content_type = "text/csv"
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Principal = {
        Service = "lambda.amazonaws.com"
      },
      Effect = "Allow",
      Sid    = ""
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_s3_attach" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_lambda_function" "sales_analyzer" {
  function_name    = "analyze_sales_data"
  filename         = "${path.module}/lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/lambda.zip")
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.11"
  timeout          = 30

  environment {
    variables = {
      INPUT_BUCKET = "data-analyst-demo-roly"
      INPUT_KEY    = "input/sales.csv"
      OUTPUT_KEY   = "output/sales_summary.csv"
    }
  }
}

terraform {
  backend "s3" {
    bucket = "data-analyst-demo-roly"
    key    = "lambda-terraform-state/terraform.tfstate"
    region = "us-east-1"
  }
}
