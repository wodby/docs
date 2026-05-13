# Kubernetes cluster infrastructure

Wodby provides core cluster capabilities through infrastructure apps deployed during cluster creation.

These infrastructure apps can include:

- Envoy Gateway
- Monitoring
- FRPC proxy tunnel for secure connection to the Kubernetes API
- Additional controller applications (e.g. AWS Load Balancer controller for EKS cluster)

Infrastructure apps follow the same general stack-and-version model as regular apps, so they can be upgraded and configured. Their configuration surface is narrower than a normal user application.

New clusters use Envoy Gateway for public HTTP, HTTPS, TCP, and UDP entrypoints. Older clusters may still run Ingress Nginx until their cluster infrastructure is upgraded.

## Infrastructure versions

### 2.0.0

Ingress Nginx was replaced with Envoy Gateway for public HTTP, HTTPS, TCP, and UDP entrypoints.

### 1.0.0

Introduced FRPC as the reverse proxy client used to connect to the Kubernetes API.

### 0.1.0

The first version of the Kubernetes cluster infrastructure.
