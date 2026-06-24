# Amazon Web Services

Wodby AWS integrations can be used for EKS clusters, RDS managed databases, S3 backup storage, SES SMTP relay, and
variables. Select only the integration kinds you need, and grant permissions for those kinds.

## Auth

For EKS, RDS, S3, and variables, use an IAM access key pair and an AWS region. The access key belongs to the AWS identity
whose permissions are described below.

SES is different: Wodby uses the Amazon SES SMTP interface, so SES integrations use Amazon SES SMTP credentials instead
of regular AWS API access keys. See [SES](#ses).

## Required Permissions

Required AWS permissions depend on the selected integration kind. If one AWS integration is used for multiple AWS API
features, the IAM user needs the combined permissions for those features. Use separate integrations when credential types
or permission scopes should differ, especially for SES.

| Integration kind | Credentials | Permissions |
| --- | --- | --- |
| EKS | IAM access key pair | Attach [AmazonEC2FullAccess](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEC2FullAccess.html), [AWSCloudFormationFullAccess](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSCloudFormationFullAccess.html), [IAMFullAccess](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/IAMFullAccess.html), and the [custom EKS policy](#custom-eks-policy). |
| RDS | IAM access key pair | Attach [AmazonEC2FullAccess](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEC2FullAccess.html), [AWSCloudFormationFullAccess](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSCloudFormationFullAccess.html), and the [custom RDS policy](#custom-rds-policy). |
| S3 | IAM access key pair | Use the [custom S3 backup policy](#custom-s3-backup-policy). [AmazonS3FullAccess](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonS3FullAccess.html) also works, but grants more access than Wodby needs for backups. |
| SES | Amazon SES SMTP credentials | The IAM user behind the SMTP credentials must be allowed to send through SES. See the [SES send policy](#ses-send-policy). |
| Variables | IAM access key pair | No AWS API permissions are required by Wodby. The integration only exposes the configured values to apps or stacks. |

AWS managed policy contents are maintained by AWS and can change over time. Attach AWS managed policies by name instead
of copying their JSON into your own customer-managed policies.

## EKS

Wodby provides a native integration with Amazon Elastic Kubernetes Service.

- Wodby creates CloudFormation stacks for the VPC, networking, EKS control plane, add-ons, and default node group.
- New EKS clusters are created across multiple Availability Zones in the selected region.
- Wodby installs AWS Load Balancer Controller and Envoy Gateway, with one Network Load Balancer used for public app
  entrypoints.
- Node disk size is configurable during cluster creation.
- Wodby deploys Metrics Server for basic Kubernetes monitoring.
- The node type selector shows only instance types Wodby supports for EKS: x86_64 instances available in the selected
  zone with more than 1 CPU, more than 4 GiB RAM, at most 32 GiB RAM, and without unsupported accelerator, Mac, or
  burstable families.

### Storage

Persistent storage is provided by Amazon Elastic Block Store through the default storage class. Wodby creates one EBS
volume for each persistent volume claim.

## RDS

Wodby provides a native integration with Amazon Relational Database Service.

- Wodby supports MySQL, MariaDB, and PostgreSQL.
- Wodby uses CloudFormation stacks to create and manage RDS resources.
- RDS instances can be created in a Wodby-managed VPC or in the VPC of an EKS cluster created under the same AWS
  integration.
- Wodby-created RDS resources use the `wodby-rds-` prefix.
- Database servers can be highly available with RDS Multi-AZ, or zonal when high availability is disabled.
- Wodby uses the `standard` RDS storage type.
- Storage size is configured during database creation. Wodby does not configure RDS storage autoscaling for these
  instances.
- You can manage databases and database users from the Wodby dashboard.

## S3

Wodby provides a native integration with Amazon Simple Storage Service. You can use S3 to store app and database backups.

- Wodby can list available S3 buckets for the connected account.
- When configuring backups, select the bucket only. Wodby resolves the selected bucket's region automatically.
- The storage class override is optional. If you leave it empty, the bucket's default storage class is used.
- Supported storage classes are `STANDARD`, `STANDARD_IA`, `ONEZONE_IA`, `INTELLIGENT_TIERING`, `GLACIER`,
  `GLACIER_IR`, and `DEEP_ARCHIVE`.
- Wodby creates pre-signed S3 URLs for backup upload, download, and restore operations.
- Wodby backups do not use AWS Lambda or S3 Object Lambda.

If backups are stored in archive classes such as `GLACIER` or `DEEP_ARCHIVE`, AWS requires restoring the archived object
before it can be read for a Wodby download or restore.

## SES

Wodby provides a native integration with Amazon Simple Email Service. You can connect SMTP services such as OpenSMTPD to
use SES as a relay for outbound emails.

For SES, use Amazon SES SMTP credentials, not regular AWS API credentials. Amazon SES SMTP credentials are
region-specific and are not the same as the AWS secret access key. In the Wodby AWS integration form:

- `Access Key ID` should be the SES SMTP user name.
- `Secret Access Key` should be the SES SMTP password.
- `Region` should match the SES SMTP credentials' region.

If you also use AWS API features such as EKS, RDS, or S3, create a separate AWS integration for SES because the secret
value for SES must be an SMTP password.

You must also verify the sender identity in Amazon SES and make sure the AWS account is allowed to send to your intended
recipients according to your SES sandbox or production sending status.

## Variables

AWS integrations can also be used as a `variable` provider. When you attach the integration to an app service or stack,
Wodby exposes:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`

## Policy Reference

Use these customer-managed policies only when the permission matrix above asks for a custom policy.

### Custom EKS Policy

Create this policy and attach it to the IAM user used by Wodby for EKS integrations.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "eks:*",
      "Resource": "*"
    }
  ]
}
```

### Custom RDS Policy

Create this policy and attach it to the IAM user used by Wodby for RDS integrations.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "rds:*",
      "Resource": "*"
    }
  ]
}
```

### Custom S3 Backup Policy

The connected AWS credentials must be able to:

- list buckets for bucket selection: `s3:ListAllMyBuckets` on `*`
- get the selected bucket location: `s3:GetBucketLocation` on `arn:aws:s3:::BUCKET_NAME`
- upload backup objects: `s3:PutObject` on `arn:aws:s3:::BUCKET_NAME/*`
- read backup objects for downloads and restores: `s3:GetObject` on `arn:aws:s3:::BUCKET_NAME/*`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:ListAllMyBuckets",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "s3:GetBucketLocation",
      "Resource": "arn:aws:s3:::BUCKET_NAME"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::BUCKET_NAME/*"
    }
  ]
}
```

Replace `BUCKET_NAME` with each bucket used as a Wodby backup destination.

AWS's managed `AmazonS3FullAccess` policy includes `s3-object-lambda:*`. Wodby backups do not use S3 Object Lambda, so
that permission is not required when you use a custom policy.

### SES Send Policy

The IAM user behind the SES SMTP credentials must be allowed to send email through SES. The minimum send action for the
SES SMTP interface is:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ses:SendRawEmail",
      "Resource": "*"
    }
  ]
}
```
