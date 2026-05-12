# 🔷 Azure Cheatsheet

> az CLI, core services, and production patterns — VMs to AKS to Functions.

---

## 🔐 Authentication & Config

```bash
az login                                              # Interactive login
az login --service-principal -u APP_ID -p SECRET --tenant TENANT_ID
az account list -o table                              # List subscriptions
az account set -s "subscription-id"                   # Set subscription
az account show                                       # Current context
az configure --defaults group=myRG location=eastus    # Set defaults
```

## 🖥️ Virtual Machines

```bash
az vm list -o table
az vm create -g myRG -n myVM --image Ubuntu2204 \
  --size Standard_B2s --admin-username azureuser \
  --generate-ssh-keys --public-ip-sku Standard
az vm start -g myRG -n myVM
az vm stop -g myRG -n myVM
az vm deallocate -g myRG -n myVM                     # Stop billing
az vm delete -g myRG -n myVM --yes
az ssh vm -g myRG -n myVM
az vm list-sizes -l eastus -o table                  # Available sizes

# Scale Sets (auto-scaling)
az vmss list -o table
az vmss scale -g myRG -n myVMSS --new-capacity 5
```

## ☸️ AKS (Kubernetes)

```bash
az aks list -o table
az aks create -g myRG -n myAKS --node-count 3 \
  --node-vm-size Standard_D4s_v3 \
  --enable-cluster-autoscaler --min-count 2 --max-count 10 \
  --network-plugin azure --generate-ssh-keys
az aks get-credentials -g myRG -n myAKS
az aks scale -g myRG -n myAKS --node-count 5
az aks nodepool list -g myRG --cluster-name myAKS -o table
az aks upgrade -g myRG -n myAKS --kubernetes-version 1.28
az aks delete -g myRG -n myAKS --yes
```

## 📦 Blob Storage

```bash
az storage account list -o table
az storage account create -n mystorageacct -g myRG \
  -l eastus --sku Standard_LRS --kind StorageV2
az storage container create -n mycontainer --account-name mystorageacct
az storage blob upload --file data.tar.gz -c mycontainer \
  -n data.tar.gz --account-name mystorageacct
az storage blob download -c mycontainer -n data.tar.gz \
  -f ./data.tar.gz --account-name mystorageacct
az storage blob list -c mycontainer --account-name mystorageacct -o table
az storage blob sync -c mycontainer -s ./dir --account-name mystorageacct
```

## 🗄️ Azure SQL & Databases

```bash
# Azure SQL
az sql server list -o table
az sql server create -g myRG -n mysqlserver \
  -u sqladmin -p 'Password123!' -l eastus
az sql db create -g myRG -s mysqlserver -n mydb \
  --service-objective S0
az sql db list -g myRG -s mysqlserver -o table

# Cosmos DB (globally distributed NoSQL)
az cosmosdb create -g myRG -n mycosmosdb --kind GlobalDocumentDB
az cosmosdb list -o table

# Azure Cache for Redis
az redis create -g myRG -n myredis -l eastus --sku Basic --vm-size c0
```

## 🌐 Networking

```bash
# VNet
az network vnet list -o table
az network vnet create -g myRG -n myVNet --address-prefix 10.0.0.0/16
az network vnet subnet create -g myRG --vnet-name myVNet \
  -n appSubnet --address-prefixes 10.0.1.0/24

# NSG (Security Groups)
az network nsg list -o table
az network nsg rule create -g myRG --nsg-name myNSG -n AllowHTTP \
  --priority 100 --access Allow --protocol Tcp --destination-port-ranges 80 443

# Application Gateway / Load Balancer
az network application-gateway list -o table
az network lb list -o table

# DNS
az network dns zone list -o table
az network dns record-set a add-record -g myRG -z example.com \
  -n www -a 1.2.3.4
```

## 📊 Azure Monitor

```bash
az monitor metrics list --resource /subscriptions/.../myVM \
  --metric "Percentage CPU" --interval PT1M
az monitor alert list -o table
az monitor log-analytics workspace list -o table
az monitor activity-log list --offset 1h -o table
```

## 🔐 Key Vault & IAM

```bash
# Key Vault
az keyvault create -g myRG -n myKeyVault -l eastus
az keyvault secret set --vault-name myKeyVault -n dbPassword --value "secret"
az keyvault secret show --vault-name myKeyVault -n dbPassword
az keyvault secret list --vault-name myKeyVault -o table

# IAM
az role assignment list -g myRG -o table
az role assignment create --assignee user@example.com \
  --role "Contributor" -g myRG
az ad user list -o table
```

## ⚡ Functions & App Service

```bash
# Functions
az functionapp create -g myRG -n myFunc \
  --runtime python --runtime-version 3.11 \
  --storage-account mystorageacct --consumption-plan-location eastus
az functionapp list -o table

# App Service
az webapp create -g myRG -p myPlan -n myWebApp --runtime "NODE:20-lts"
az webapp list -o table
az webapp log tail -g myRG -n myWebApp
```

## 🆚 Azure vs AWS Quick Map

```
Azure                    AWS Equivalent
─────────────────────────────────────────
Virtual Machines         EC2
AKS                      EKS
Blob Storage             S3
Azure SQL                RDS
Cosmos DB                DynamoDB
Functions                Lambda
App Service              Elastic Beanstalk
Azure Monitor            CloudWatch
Key Vault                Secrets Manager
Active Directory         IAM
Application Gateway      ALB
Front Door               CloudFront
Azure DevOps             CodePipeline
Logic Apps               Step Functions
```

## 🎯 FAANG Interview Q&A

```
Q: When would you choose Azure over AWS?
A: Microsoft enterprise ecosystem (Active Directory, Office 365),
   .NET workloads, hybrid cloud (Azure Arc, Stack),
   strong compliance certifications (government, healthcare).

Q: What's the difference between Azure AD and AWS IAM?
A: Azure AD: full identity provider (SSO, MFA, B2C, SAML/OIDC).
   AWS IAM: resource access control (policies, roles, groups).
   Azure AD is broader — identity + directory service.

Q: Explain Cosmos DB consistency levels.
A: Strong → Bounded Staleness → Session → Consistent Prefix → Eventual
   Maps to the CAP theorem spectrum. Session consistency is the
   default and most commonly used (read-your-writes).
```

---

> 💡 **Azure Strength:** Best hybrid cloud story (Azure Arc), tight enterprise integration (AD, O365), and strong compliance certifications. Choose Azure when enterprise identity management is critical.
