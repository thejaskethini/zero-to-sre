# ☁️ Cloud CLI Cheatsheet

> AWS CLI · Azure CLI · gcloud — side by side.

---

## 🔐 Authentication

| Action | AWS | Azure | GCP |
|--------|-----|-------|-----|
| Login | `aws configure` | `az login` | `gcloud auth login` |
| Who am I? | `aws sts get-caller-identity` | `az account show` | `gcloud config list` |
| Set region | `aws configure set region us-east-1` | `az account set -s <id>` | `gcloud config set project <id>` |
| List profiles | `aws configure list-profiles` | `az account list -o table` | `gcloud config configurations list` |

## 🖥️ Compute

| Action | AWS | Azure | GCP |
|--------|-----|-------|-----|
| List VMs | `aws ec2 describe-instances` | `az vm list -o table` | `gcloud compute instances list` |
| Create VM | `aws ec2 run-instances --image-id ami-xxx --instance-type t3.micro` | `az vm create -g myRG -n myVM --image Ubuntu2204` | `gcloud compute instances create myvm --machine-type=e2-micro` |
| Start VM | `aws ec2 start-instances --instance-ids i-xxx` | `az vm start -g myRG -n myVM` | `gcloud compute instances start myvm` |
| Stop VM | `aws ec2 stop-instances --instance-ids i-xxx` | `az vm stop -g myRG -n myVM` | `gcloud compute instances stop myvm` |
| SSH | `ssh -i key.pem ec2-user@<ip>` | `az ssh vm -g myRG -n myVM` | `gcloud compute ssh myvm` |

## 📦 Storage

| Action | AWS (S3) | Azure (Blob) | GCP (GCS) |
|--------|----------|-------------|-----------|
| List buckets | `aws s3 ls` | `az storage account list -o table` | `gsutil ls` |
| Upload | `aws s3 cp file s3://bucket/` | `az storage blob upload --file file -c cont -n file` | `gsutil cp file gs://bucket/` |
| Download | `aws s3 cp s3://bucket/file .` | `az storage blob download -c cont -n file -f file` | `gsutil cp gs://bucket/file .` |
| Sync | `aws s3 sync . s3://bucket/` | `az storage blob sync -c cont -s ./dir` | `gsutil rsync -r . gs://bucket/` |

## ☸️ Kubernetes

| Action | AWS (EKS) | Azure (AKS) | GCP (GKE) |
|--------|-----------|-------------|-----------|
| List clusters | `aws eks list-clusters` | `az aks list -o table` | `gcloud container clusters list` |
| Get kubeconfig | `aws eks update-kubeconfig --name cl` | `az aks get-credentials -g rg -n cl` | `gcloud container clusters get-credentials cl` |
| Create cluster | `eksctl create cluster --name cl` | `az aks create -g rg -n cl --node-count 3` | `gcloud container clusters create cl --num-nodes=3` |

## 🌐 Networking

| Action | AWS | Azure | GCP |
|--------|-----|-------|-----|
| List VPCs/VNets | `aws ec2 describe-vpcs` | `az network vnet list -o table` | `gcloud compute networks list` |
| List subnets | `aws ec2 describe-subnets` | `az network vnet subnet list -g rg --vnet-name vn` | `gcloud compute networks subnets list` |
| List IPs | `aws ec2 describe-addresses` | `az network public-ip list -o table` | `gcloud compute addresses list` |

## 💰 Cost

| Action | AWS | Azure | GCP |
|--------|-----|-------|-----|
| Check cost | `aws ce get-cost-and-usage ...` | `az consumption usage list ...` | `gcloud billing accounts list` |
| Set budget | Console → Billing → Budgets | `az consumption budget create ...` | `gcloud billing budgets create ...` |

---

> 💡 **Tip:** Install all three CLIs and practice switching between them. Multi-cloud fluency is a high-value skill.
