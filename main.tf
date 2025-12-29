terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable APIs
resource "google_project_service" "cloudrun" {
  service = "run.googleapis.com"
}

resource "google_project_service" "firestore" {
  service = "firestore.googleapis.com"
}

# Firestore Database (Default)
resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = "(default)"
  location_id = "nam5" # US Multi-region, or use var.region if preferred for regional
  type        = "FIRESTORE_NATIVE"

  depends_on = [google_project_service.firestore]
}

# Cloud Run Service
resource "google_cloud_run_v2_service" "salo_landing_page" {
  name     = "salo-landing-page"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "gcr.io/${var.project_id}/salo-landing-page:latest"
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }
  }

  depends_on = [google_project_service.cloudrun]
}

# Allow public access to the Cloud Run service
resource "google_cloud_run_v2_service_iam_member" "public_access" {
  name     = google_cloud_run_v2_service.salo_landing_page.name
  location = google_cloud_run_v2_service.salo_landing_page.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Output the Cloud Run URL
output "service_url" {
  value = google_cloud_run_v2_service.salo_landing_page.uri
}
