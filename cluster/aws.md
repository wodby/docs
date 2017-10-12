# Kubernetes cluster on AWS

![Cluster schema](_images/wodby-aws-cluster.png)

## AWS Services:

* Route53 
* AWS Certificate Manager
* Elastic Load Balancing (ELB)
* Elastic Compute Cloud (EC2)
* Relational Database Service (RDS)
* Amazon Elastic File System (EFS) or Simple Storage Service (S3)
* Optional: CloudFront CDN
* Optional: ElastiCache

## Basic concept

* Domains will be hosted on Route53
* SSL certificates will be managed via AWS Certificate Manager
* Database server could be RDS or stateful container deployed to EC2 (only single AZ)
* Files can be stored on EFS or on S3 (requires integration on app side)
* CloudFront CDN can be used in pair with S3 storage
* CI/CD workflow required for deployments
* Scalability can be on container level and node level
* Cluster will run under your AWS account
* Additional applications deployed to cluster will cost you additional money (ELB, traffic, usage) 
* For HA/FT setup RDS used as DB server and EFS / S3 used as a file storage  

## Optional features

* Centralized log streaming to Elasticsearch
* Monitoring and alerting via Grafana
* Integration with ElastiCache as scalable cache storage