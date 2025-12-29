variable "project_id" {
  description = "The GCP project ID"
  type        = string
  default     = "sales-edu-480702"
}

variable "region" {
  description = "The GCP region to deploy to"
  type        = string
  default     = "us-central1"
}

variable "build_id" {
  description = "A unique ID to force a new deployment (e.g. timestamp)"
  type        = string
  default     = "default"
}
