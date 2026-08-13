terraform {
  required_version = ">= 1.11, < 2.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  profile = "platform-lab"
  region  = "eu-north-1"
}

data "aws_caller_identity" "current" {}

output "aws_account_id" {
  description = "AWS account ID for the authenticated caller."
  value       = data.aws_caller_identity.current.account_id
}

output "caller_arn" {
  description = "ARN of the authenticated AWS caller."
  value       = data.aws_caller_identity.current.arn
}
