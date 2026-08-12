terraform {
  required_version = ">= 1.11, < 2.0"
}

variable "service_name" {
  description = "Name used to identify this service in future infrastructure."
  type        = string
  default     = "service-health"
}

locals {
  foundation_message = "OpenTofu foundation for ${var.service_name}"
}

output "foundation_message" {
  description = "Confirms that OpenTofu can evaluate this provider-free module."
  value       = local.foundation_message
}
