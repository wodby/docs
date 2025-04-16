# Kubernetes cluster infrastructure

We manage Kubernetes cluster capabilities by deploying special system application – infrastructure applications during a cluster creation. Right now, we deploy the following stacks:

- Ingress Nginx
- Monitoring
- Proxy tunnel for secure connection to Kubernetes API
- Additional controller applications (e.g. AWS Load Balancer controller for EKS cluster)

Infrastructure apps are similar to usual apps in a way that they can be upgraded and configured (although not as extension as users' apps).   
