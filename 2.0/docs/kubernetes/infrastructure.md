# Kubernetes cluster infrastructure

Wodby provides core cluster capabilities through infrastructure apps deployed during cluster creation.

These infrastructure apps can include:

- Ingress Nginx
- Monitoring
- Proxy tunnel for secure connection to Kubernetes API
- Additional controller applications (e.g. AWS Load Balancer controller for EKS cluster)

Infrastructure apps follow the same general stack-and-version model as regular apps, so they can be upgraded and configured. Their configuration surface is narrower than a normal user application.
