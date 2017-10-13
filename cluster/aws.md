# Kubernetes cluster on AWS

![Cluster schema](_images/wodby-aws-cluster.png)

## AWS Services:

* Route53 
* AWS Certificate Manager
* Elastic Load Balancing (ELB)
* Elastic Compute Cloud (EC2)
* Relational Database Service (RDS)
* Amazon Elastic File System (EFS) or Simple Storage Service (S3)
* Optional: CloudFront CDN, ElastiCache

## Basic concept

* We set up the cluster under your AWS account
* Domains will be hosted on Route53
* SSL certificates will be managed via AWS Certificate Manager
* Database server could be RDS (recommended) or stateful container deployed to EC2 (only single AZ)
* Files can be stored on EFS or S3, the latter requires integration on an application level
* CloudFront CDN can be used in pair with S3 storage 
* CI/CD workflow required for deployments

## Optional features

* Centralized log streaming to Elasticsearch
* Monitoring and alerting via Grafana
* Integration with ElastiCache as scalable HA cache storage
* Reverse caching proxy setup for consistent cache storage
* CloudFront (or any third-party CDN) configuration for EFS