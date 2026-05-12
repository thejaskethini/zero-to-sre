# ☁️ GCP (Google Cloud) Cheatsheet

> gcloud CLI, core services, and production patterns — from Compute Engine to GKE to BigQuery.

---

## 🔐 Authentication & Config

```bash
gcloud auth login                                     # Interactive login
gcloud auth activate-service-account --key-file=sa.json  # Service account
gcloud auth application-default login                 # ADC for local dev
gcloud config set project my-project-id
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a
gcloud config list                                    # Current config
gcloud config configurations list                     # All configs
gcloud config configurations create staging           # New config profile
gcloud config configurations activate staging
```

## 🖥️ Compute Engine (VMs)

```bash
gcloud compute instances list
gcloud compute instances create myvm \
  --machine-type=e2-medium --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud --boot-disk-size=50GB \
  --tags=http-server --zone=us-central1-a
gcloud compute instances stop myvm
gcloud compute instances start myvm
gcloud compute instances delete myvm
gcloud compute ssh myvm --zone=us-central1-a
gcloud compute scp localfile.txt myvm:/tmp/ --zone=us-central1-a

# Instance groups (auto-scaling)
gcloud compute instance-groups managed list
gcloud compute instance-groups managed set-autoscaling mygroup \
  --max-num-replicas=10 --min-num-replicas=2 \
  --target-cpu-utilization=0.7
```

## ☸️ GKE (Kubernetes)

```bash
gcloud container clusters list
gcloud container clusters create prod-cluster \
  --num-nodes=3 --machine-type=e2-standard-4 \
  --enable-autoscaling --min-nodes=2 --max-nodes=10 \
  --region=us-central1 --release-channel=regular
gcloud container clusters get-credentials prod-cluster --region=us-central1
gcloud container clusters resize prod-cluster --num-nodes=5
gcloud container node-pools list --cluster=prod-cluster
gcloud container clusters delete prod-cluster
```

## 📦 Cloud Storage (GCS)

```bash
gsutil ls                                             # List buckets
gsutil mb gs://my-bucket                              # Create bucket
gsutil cp file.tar.gz gs://my-bucket/                # Upload
gsutil cp gs://my-bucket/file.tar.gz .               # Download
gsutil rsync -r ./dir gs://my-bucket/dir             # Sync
gsutil -m cp -r ./data gs://my-bucket/               # Parallel upload (-m)
gsutil ls -l gs://my-bucket/                         # List with details
gsutil du -sh gs://my-bucket                         # Bucket size
gsutil lifecycle set lifecycle.json gs://my-bucket   # Lifecycle policy
gsutil iam ch allUsers:objectViewer gs://my-bucket   # Make public
```

## 🗄️ Cloud SQL & Databases

```bash
# Cloud SQL
gcloud sql instances list
gcloud sql instances create mydb --database-version=POSTGRES_15 \
  --tier=db-custom-2-4096 --region=us-central1 \
  --availability-type=REGIONAL                        # High availability
gcloud sql connect mydb --user=postgres
gcloud sql backups create --instance=mydb
gcloud sql export sql mydb gs://bucket/backup.sql --database=mydb

# Cloud Spanner (globally distributed)
gcloud spanner instances list
# BigQuery
bq ls                                                 # List datasets
bq query --use_legacy_sql=false 'SELECT COUNT(*) FROM `project.dataset.table`'
bq mk --dataset project:my_dataset
bq load --source_format=CSV my_dataset.table gs://bucket/data.csv
```

## 🌐 Networking

```bash
# VPC
gcloud compute networks list
gcloud compute networks create my-vpc --subnet-mode=custom
gcloud compute networks subnets create my-subnet \
  --network=my-vpc --range=10.0.1.0/24 --region=us-central1

# Firewall rules
gcloud compute firewall-rules list
gcloud compute firewall-rules create allow-http \
  --network=my-vpc --allow=tcp:80,tcp:443 --target-tags=http-server
gcloud compute firewall-rules create allow-internal \
  --network=my-vpc --allow=all --source-ranges=10.0.0.0/8

# Load Balancing
gcloud compute forwarding-rules list
gcloud compute backend-services list

# Cloud DNS
gcloud dns managed-zones list
gcloud dns record-sets list --zone=my-zone
```

## 📊 Monitoring & Logging

```bash
# Cloud Logging
gcloud logging read "resource.type=gce_instance AND severity>=ERROR" --limit=50
gcloud logging read "resource.type=k8s_container AND resource.labels.namespace_name=production" --limit=20

# Cloud Monitoring (alerting)
gcloud monitoring policies list
gcloud monitoring dashboards list

# Metrics
gcloud monitoring metrics list --filter="metric.type=compute.googleapis.com"
```

## 🔐 IAM

```bash
gcloud iam roles list --project=my-project
gcloud projects get-iam-policy my-project
gcloud projects add-iam-policy-binding my-project \
  --member="user:dev@example.com" --role="roles/editor"
gcloud iam service-accounts list
gcloud iam service-accounts create my-sa --display-name="My SA"
gcloud iam service-accounts keys create key.json --iam-account=my-sa@project.iam.gserviceaccount.com
```

## ⚡ Cloud Run & Functions

```bash
# Cloud Run (serverless containers)
gcloud run deploy my-api --image=gcr.io/project/api:latest \
  --platform=managed --region=us-central1 --allow-unauthenticated \
  --memory=512Mi --cpu=1 --max-instances=10
gcloud run services list
gcloud run services describe my-api --region=us-central1

# Cloud Functions
gcloud functions deploy my-func --runtime=python311 \
  --trigger-http --entry-point=handler --allow-unauthenticated
gcloud functions logs read my-func --limit=50
```

## 🆚 GCP vs AWS Quick Map

```
GCP                     AWS Equivalent
─────────────────────────────────────────
Compute Engine          EC2
GKE                     EKS
Cloud Storage           S3
Cloud SQL               RDS
BigQuery                Redshift + Athena
Cloud Run               Fargate + App Runner
Cloud Functions         Lambda
Cloud Pub/Sub           SNS + SQS
Cloud DNS               Route 53
Cloud Load Balancing    ALB/NLB
Cloud IAM               IAM
Cloud Monitoring        CloudWatch
Cloud Logging           CloudWatch Logs
Cloud Armor             WAF
Cloud CDN               CloudFront
```

## 🎯 FAANG Interview Q&A

```
Q: Why would you choose GCP over AWS?
A: BigQuery (best-in-class analytics), GKE (best managed K8s),
   global network (lower latency), simpler IAM model,
   strong ML/AI platform (Vertex AI). AWS wins on breadth
   of services and enterprise adoption.

Q: How does GKE differ from EKS?
A: GKE: fully managed control plane (free), auto-upgrades,
   auto-repair, built-in monitoring, Autopilot mode.
   EKS: pay for control plane, more manual setup,
   but deeper AWS integration and larger ecosystem.

Q: Explain Cloud Spanner.
A: Globally distributed, horizontally scalable relational DB
   with strong consistency. Uses TrueTime (atomic clocks)
   for global consistency. Use when: global apps needing
   ACID transactions across regions. Cost: $$$$.
```

---

> 💡 **GCP Strength:** GKE is widely considered the best managed Kubernetes service. If your workload is container-heavy, GCP is a strong choice.
