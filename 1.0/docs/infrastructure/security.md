# Security

When you connect a server, Wodby enables automatic operating-system security updates. Significant updates to the Linux kernel and Wodby-managed runtime components should be coordinated through [infrastructure maintenance](maintenance.md).

* [Infrastructure maintenance](maintenance.md)
* [Stacks maintenance](../stacks/maintenance.md)

We release unplanned updates to our infrastructure for all critical security updates and notify all affected customers by email (you cannot unsubscribe from those emails).

!!! warning "Do not independently upgrade the container runtime or Kubernetes"
    Wodby infrastructure uses coordinated, pinned versions of Docker, Kubernetes, containerd, cri-dockerd, and networking components. Uncoordinated package upgrades can make existing applications unavailable.

Keep Kubernetes API, kubelet, and etcd ports inaccessible from the public internet. Public application traffic normally requires ports 80 and 443, plus the documented NodePort range when an application exposes a direct service. See [UFW configuration](ufw.md).
