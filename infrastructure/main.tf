terraform {
  required_version = ">= 1.11, < 2.0"

  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.13.0"
    }
  }
}

provider "github" {
  owner = "MatsOSta"
}

resource "github_branch_protection" "master" {
  repository_id  = "platform-engineering-lab"
  pattern        = "master"
  enforce_admins = false

  required_status_checks {
    strict = true
    contexts = [
      "checks",
      "container-scan",
      "opentofu-validation",
    ]
  }

  required_pull_request_reviews {
    required_approving_review_count = 0
  }
}
