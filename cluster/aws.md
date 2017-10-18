# Kubernetes cluster on AWS

[![Cluster schema](_images/aws-cluster-schema.png)](_images/aws-cluster-schema.png)

## AWS Services:

* Virtual Private Cloud (VPC)
* Elastic Load Balancing (ELB)
* Elastic Compute Cloud (EC2)
* Relational Database Service (RDS)
* Amazon Elastic File System (EFS)
* Additional: Simple Safe Storage (S3), ElastiCache, Route53, Certificate Manager, CloudFront

## Basic concept

* Single AZ or multi-AZ (fault tolerance) setups
* Database server could be RDS (recommended) or stateful container deployed to EC2 (only single AZ)
* Static files stored on EFS
* CI/CD workflow required for deployments

#### Optional

* CloudFront CDN integration 
* Domains can be hosted on Route53
* SSL certificates can be managed via AWS Certificate Manager
* Centralized log streaming to Elasticsearch
* Monitoring and alerting via Grafana