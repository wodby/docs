# Kubernetes Cluster

In addition to our single server infrastructure setup we offer a Kubernetes cluster solution. Currently, we offer cluster setup only for public clouds (AWS, GCP, Azure). Only specific stacks / services provided by Wodby are suitable for cluster deployment.

Setup and maintenance of the cluster is significantly more complex and expensive than a single-server setup. Normally we recommend cluster setups only if you need one of the following:

#### Scalability

> If you're not sure whether a single server is enough to handle your load, this probably means you don't need a cluster.

There two types of scalability for: 

1. Stateless services. These services don't care how many replicas are running and on which node (have no state). Can be flexibly scheduled across a pool of auto-scaled nodes. Stateless services can be scaled manually (# of replicas) or automatically (based on resources consumption). Examples: http server, php-fpm.

2. Stateful services. Run on specific nodes (have state) and require additional individual configuration for scalability (read replicas, sharding). Examples: any DBMS, Elasticsearch. Usually public clouds provide scalable stateful services that come with high-availability out of the box (e.g. AWS RDS, ElastiCache). 

#### High availability

With high availability setup you can be sure that if one specific node goes down, your application will recover. Services can be restored rapidly but not instantaneously. Suitable for applications that must be restored quickly and can withstand a short interruption should a failure occur.

1. Stateless services configured for auto scheduling across a pool of nodes. New nodes spun up automatically when requested
2. Stateful services configured with high availability (master-master, master-slave setup) or replaced by public cloud  managed services with built-in high availability

If entire cloud provider's availability zone goes down (unplanned outages), your application goes down. 

#### Fault tolerance

A fault tolerant environment has no service interruption but a significantly higher cost. We simultaneously run two complete copies of infrastructure in multiple availability zones (inside the same region) provided by public cloud. The chance that two availability zones simultaneously goes down is extremely low but for extra high availability, infrastructure can be deployed across multiple regions. 

## Kubernetes cluster on AWS

![Cluster schema](_images/wodby-aws-cluster.png)

#### AWS Services:

* Route53 
* AWS Certificate Manager
* Elastic Load Balancing (ELB)
* Elastic Compute Cloud (EC2)
* Relational Database Service (RDS)
* Amazon Elastic File System (EFS) or Simple Storage Service (S3)
* Optional: CloudFront CDN
* Optional: ElastiCache

#### Basic concept

* Domains will be hosted on Route53
* SSL certificates will be managed via AWS Certificate Manager
* Database server could be RDS or stateful container deployed to EC2 (only single AZ)
* Files can be stored on EFS or on S3 (requires integration on app side)
* CloudFront CDN can be used for S3 storage
* CI/CD workflow required for deployments
* Scalability can be on container level and node level
* Cluster will run under your AWS account
* Additional applications deployed to cluster will cost you additional money (ELB, traffic, usage) 
* For HA/FT setup RDS used as DB server and EFS / S3 used as a file storage  

#### Optional features

* Centralized log streaming to Elasticsearch
* Monitoring and alerting via Grafana
* Integration with ElastiCache as scalable cache storage