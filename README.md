# SalO Landing Page

A premium landing page for **SalO**, the sales intelligence agent integrated with Slack.

## Deployment to Google Cloud Run

This project is configured for deployment to Google Cloud Run with Firestore lead storage.

### Prerequisites
- [Google Cloud SDK (gcloud)](https://cloud.google.com/sdk/docs/install) installed and authenticated.
- [Terraform](https://www.terraform.io/downloads.html) installed.
- Access to GCP Project ID: `sales-edu-480702`

### 1. Configure GCP Account and Project
Ensure you are using the correct account and project. Run:

```bash
gcloud auth login igormolybog@gmail.com
gcloud config set project sales-edu-480702
gcloud auth application-default login
```

If you get a "quota project" warning, you can run:
```bash
gcloud auth application-default set-quota-project sales-edu-480702
```

#### ⚠️ IAM Permissions Notice
If you receive a `PERMISSION_DENIED` error, ensure that `igormolybog@gmail.com` has the following roles in the [GCP Console IAM page](https://console.cloud.google.com/iam-admin/iam):
- **Cloud Build Editor** (`roles/cloudbuild.builds.editor`)
- **Storage Admin** (`roles/storage.admin`) — *required for uploading the source code*
- **Cloud Run Admin** (`roles/run.admin`) — *required for Terraform to deploy*
- **Firestore Admin** (`roles/datastore.owner`) — *required for Terraform to create the database*
- **Service Usage Consumer** (`roles/serviceusage.serviceUsageConsumer`)

### 2. Build and Push Container
Build the Docker image and push it to Google Container Registry:

```bash
gcloud builds submit --tag gcr.io/sales-edu-480702/salo-landing-page
```

### 3. Deploy Infrastructure with Terraform
Navigate to the project root and run:

```bash
terraform init
terraform apply -var="project_id=sales-edu-480702"
```

### 4. Cleanup
To stop the local dev server, use `Ctrl+C`. To destroy the cloud infrastructure:

```bash
terraform destroy -var="project_id=sales-edu-480702"
```

## Local Hosting
... (previous instructions)

## File Structure
- `index.html`: Main landing page structure.
- `style.css`: Premium dark-mode styles and animations.
- `assets/`: Directory for images and icons.

## Security & Privacy
SalO is built with a security-first mindset. No data is ever shared outside of your organization.
