# ☁️ AWS Production Cheatsheet

> The AWS services, CLI commands, and architectural patterns that FAANG-level SREs use daily in production.

---

## 🖥️ EC2 & Compute

```bash
# Instance management
aws ec2 describe-instances --filters "Name=tag:Environment,Values=production" \
  --query "Reservations[].Instances[].[InstanceId,State.Name,PrivateIpAddress,Tags[?Key=='Name'].Value|[0]]" \
  --output table
aws ec2 start-instances --instance-ids i-0abc123
aws ec2 stop-instances --instance-ids i-0abc123
aws ec2 reboot-instances --instance-ids i-0abc123
aws ec2 terminate-instances --instance-ids i-0abc123

# SSM (no SSH keys needed — FAANG standard)
aws ssm start-session --target i-0abc123
aws ssm send-command --targets "Key=tag:Environment,Values=production" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["uptime","free -h","df -h"]'

# Auto Scaling
aws autoscaling describe-auto-scaling-groups --output table
aws autoscaling set-desired-capacity --auto-scaling-group-name prod-asg --desired-capacity 10
aws autoscaling update-auto-scaling-group --auto-scaling-group-name prod-asg \
  --min-size 3 --max-size 20 --desired-capacity 5
```

## 📦 S3

```bash
aws s3 ls                                            # List buckets
aws s3 ls s3://my-bucket --recursive --summarize     # Bucket size
aws s3 cp file.tar.gz s3://my-bucket/backups/        # Upload
aws s3 sync ./dist s3://my-bucket/static/ --delete   # Sync directory
aws s3 presign s3://my-bucket/file.zip --expires-in 3600  # Signed URL (1h)
aws s3api put-bucket-versioning --bucket my-bucket \
  --versioning-configuration Status=Enabled          # Enable versioning
```

## 🗄️ RDS & Databases

```bash
# Instance management
aws rds describe-db-instances \
  --query "DBInstances[].[DBInstanceIdentifier,DBInstanceStatus,Engine,Endpoint.Address]" \
  --output table
aws rds create-db-snapshot --db-instance-identifier prod-db \
  --db-snapshot-identifier prod-db-$(date +%Y%m%d)
aws rds reboot-db-instance --db-instance-identifier prod-db

# Failover (Multi-AZ)
aws rds reboot-db-instance --db-instance-identifier prod-db --force-failover

# Performance Insights
aws pi get-resource-metrics --service-type RDS \
  --identifier db-XXXXX --metric-queries file://metrics.json
```

## 🌐 ELB & Networking

```bash
# Load Balancer
aws elbv2 describe-load-balancers --output table
aws elbv2 describe-target-health --target-group-arn arn:aws:...
aws elbv2 register-targets --target-group-arn arn:aws:... \
  --targets Id=i-0abc123

# VPC & Security Groups
aws ec2 describe-vpcs --output table
aws ec2 describe-security-groups --group-ids sg-xxx \
  --query "SecurityGroups[].IpPermissions[]"
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-xxx" --output table

# Route 53
aws route53 list-hosted-zones
aws route53 change-resource-record-sets --hosted-zone-id Z123 \
  --change-batch file://dns-change.json
```

## 📊 CloudWatch & Monitoring

```bash
# Alarms
aws cloudwatch describe-alarms --state-value ALARM --output table
aws cloudwatch set-alarm-state --alarm-name "High-CPU" \
  --state-value OK --state-reason "Manual reset"

# Metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-0abc123 \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 --statistics Average

# Logs
aws logs describe-log-groups
aws logs tail /aws/lambda/my-function --follow --since 1h
aws logs filter-log-events --log-group-name /ecs/api \
  --filter-pattern "ERROR" --start-time $(date -d '1 hour ago' +%s000)
```

## ☸️ EKS (Kubernetes on AWS)

```bash
aws eks list-clusters
aws eks update-kubeconfig --name prod-cluster --region us-east-1
aws eks describe-cluster --name prod-cluster \
  --query "cluster.[status,version,endpoint]"

# Node groups
aws eks list-nodegroups --cluster-name prod-cluster
aws eks update-nodegroup-config --cluster-name prod-cluster \
  --nodegroup-name workers --scaling-config minSize=3,maxSize=10,desiredSize=5
```

## 🔐 IAM & Security

```bash
# Who am I?
aws sts get-caller-identity

# Assume role
aws sts assume-role --role-arn arn:aws:iam::123:role/admin \
  --role-session-name debug-session

# List users & policies
aws iam list-users --output table
aws iam list-attached-user-policies --user-name deploy
aws iam list-access-keys --user-name deploy

# Security audit
aws iam generate-credential-report
aws iam get-credential-report --output text --query Content | base64 -d
```

## 💰 Cost Management

```bash
# Current month cost
aws ce get-cost-and-usage \
  --time-period Start=$(date +%Y-%m-01),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE

# Cost by tag
aws ce get-cost-and-usage \
  --time-period Start=2026-01-01,End=2026-02-01 \
  --granularity MONTHLY --metrics BlendedCost \
  --group-by Type=TAG,Key=Environment
```

---

> 💡 **FAANG Rule:** Use SSM instead of SSH. Tag everything. Enable CloudTrail and GuardDuty on day one. Never use root credentials. Use Organizations for multi-account strategy.
