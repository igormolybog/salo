# FinAgent landing page

A premium landing page for **FinAgent** — early concept for an AI agent that monitors your complete financial picture and executes within guardrails you set. Deployed to Google Cloud Run with Firestore lead capture for the waitlist.

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

#### Multiple accounts (e.g. Gmail + university)
You do **not** need to log out of `molybog@hawaii.edu`. `gcloud auth login` adds credentials; multiple accounts can coexist. Switch the active account for this terminal with:

```bash
gcloud config set account igormolybog@gmail.com
gcloud config set project sales-edu-480702
```

Or use **named configurations** so one profile is Gmail + this project and another stays Hawaii:

```bash
gcloud config configurations create salo-gmail --activate
gcloud config set account igormolybog@gmail.com
gcloud config set project sales-edu-480702
# Later: gcloud config configurations activate default   # back to Hawaii
```

Application Default Credentials (used by Terraform / Firestore locally) are separate: run `gcloud auth application-default login` while the Gmail configuration is active, or point `GOOGLE_APPLICATION_CREDENTIALS` at a service account key if you use one.

If you use a helper such as `g-switch`, keep using it — it is doing the same kind of account/project switching without removing other logged-in identities.

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

### 4. Updating the App (Forcing a Redeploy)
To force a new deployment and ensure Cloud Run pulls the latest image, run:

```bash
terraform apply -var="project_id=sales-edu-480702" -var="build_id=$(date +%s)"
```

*This command sends a unique timestamp to Terraform, which triggers a fresh deployment of your `:latest` image every time.*

### 5. Tracking and Analytics
You can track conversions (page views vs. CTA clicks) directly in **Cloud Logging**.

1. Go to **Cloud Run** > **salo-landing-page** > **Logs**.
2. In the query box, you can filter for specific events:
   - `jsonPayload.event = "page_view"` (home and signup page loads)
   - `jsonPayload.event = "cta_click"` (waitlist CTAs: `nav_join_waitlist`, `hero_join_waitlist`)
   - `jsonPayload.metadata.product = "finagent"`
3. To see the funnel, you can create a **Log-based Metric**:
   - Go to **Logging** > **Log-based Metrics**.
   - Create a metric for each event to see them in a Dashboard.

### 6. Cleanup
To stop the local dev server, use `Ctrl+C`. To destroy the cloud infrastructure:

```bash
terraform destroy -var="project_id=sales-edu-480702"
```

## File Structure
- `index.html`: Main landing page structure.
- `signup.html`: Waitlist form.
- `style.css`: Dark-mode styles and animations.
- `resources/FinAgent_OnePager-1.pdf`: Concept one-pager (reference).

## Security & Privacy
FinAgent is designed with a security-first mindset. Waitlist data is stored in your GCP project; treat production credentials and Firestore rules accordingly.
