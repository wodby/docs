# Amazon Web Services

## Auth

Currently, the only authentication method we support is the IAM user key pair with a region specified during the integration creation. 

### Required IAM policies

IAM key for AWS integration requires the following policies:

#### 1. AmazonEC2FullAccess (AWS Managed Policy)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "ec2:*",
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "elasticloadbalancing:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "cloudwatch:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "autoscaling:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "iam:CreateServiceLinkedRole",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "iam:AWSServiceName": [
            "autoscaling.amazonaws.com",
            "ec2scheduled.amazonaws.com",
            "elasticloadbalancing.amazonaws.com",
            "spot.amazonaws.com",
            "spotfleet.amazonaws.com",
            "transitgateway.amazonaws.com"
          ]
        }
      }
    }
  ]
}
```

#### 2. AWSCloudFormationFullAccess (AWS Managed Policy)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:*"
      ],
      "Resource": "*"
    }
  ]
}
```

#### 3. IAMFullAccess (AWS Managed Policy)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iam:*",
        "organizations:DescribeAccount",
        "organizations:DescribeOrganization",
        "organizations:DescribeOrganizationalUnit",
        "organizations:DescribePolicy",
        "organizations:ListChildren",
        "organizations:ListParents",
        "organizations:ListPoliciesForTarget",
        "organizations:ListRoots",
        "organizations:ListPolicies",
        "organizations:ListTargetsForPolicy"
      ],
      "Resource": "*"
    }
  ]
}
```

#### 4. EKS full access (custom policy)

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

#### 5. RDS full access:

If you plan to use Managed databases

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

## EKS

Wodby provides a native integration with Elastic Kubernetes Service. 

- EKS cluster we create always deployed with multi-az high availability in a chosen region
- We create a CloudFormation stack to create a cluster's control plane, addons and node groups.
- Micro and nano instance types forbidden due to the very low pod limit
- We create a single load balancer (NLB) per cluster and deploy an Ingress Nginx controller to manage SSL certificates
- Node disk size can be configured upon creation
- We deploy a metrics server for the basic Wodby Kubernetes monitoring

### Storage

Persistent storage is provided by Elastic Block Storage via the default storage class. We create a new block storage volume for each persistent volume claim.

## RDS

Wodby provides native integration with Relational Database Service.

- We support MySQL, MariaDB and PostgreSQL
- We use cloudformation stacks to manage all the resources
- Databases can be resided with a EKS cluster created under the same integration
- All resources we create have `wodby-rds-` prefix
- Database server can either be highly available (regional) or not (zonal)
- We use `standard` storage type
- Storage size can be configured upon creation and storage autoscaling can be enabled
- You can manage your DBs and users form Wodby dashboard

## S3

Wodby provides native integration with Simple Storage Service. You can use S3 for storing your applications' backups.
