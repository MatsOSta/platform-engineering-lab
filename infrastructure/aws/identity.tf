resource "aws_iam_openid_connect_provider" "github_actions" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = [
    "sts.amazonaws.com",
  ]

  tags = {
    Project     = "platform-engineering-lab"
    Environment = "lab"
    ManagedBy   = "OpenTofu"
  }
}

data "aws_iam_policy_document" "github_actions_trust" {
  statement {
    actions = [
      "sts:AssumeRoleWithWebIdentity",
    ]

    principals {
      type = "Federated"
      identifiers = [
        aws_iam_openid_connect_provider.github_actions.arn,
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values = [
        "sts.amazonaws.com",
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"
      values = [
        "repo:MatsOSta@112391018/platform-engineering-lab@1329830113:ref:refs/heads/master",
      ]
    }
  }
}

resource "aws_iam_role" "github_actions_identity" {
  name               = "platform-engineering-lab-github-identity"
  assume_role_policy = data.aws_iam_policy_document.github_actions_trust.json

  tags = {
    Project     = "platform-engineering-lab"
    Environment = "lab"
    ManagedBy   = "OpenTofu"
  }
}

data "aws_iam_policy_document" "github_actions_vpc_read" {
  statement {
    actions = [
      "ec2:DescribeVpcs",
    ]

    resources = ["*"]

    condition {
      test     = "StringEquals"
      variable = "aws:RequestedRegion"
      values = [
        "eu-north-1",
      ]
    }
  }
}

resource "aws_iam_role_policy" "github_actions_vpc_read" {
  name   = "platform-engineering-lab-github-vpc-read"
  role   = aws_iam_role.github_actions_identity.id
  policy = data.aws_iam_policy_document.github_actions_vpc_read.json
}
