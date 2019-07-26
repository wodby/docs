# Security

When you connect a server to Wodby we enable automatic security updates for the system. Significant updates to core Linux components (such as Linux kernel) should be performed manually by you or happen during the [upgrade of infrastructure](index.md#maintenance). We usually are very conservative when it comes to system updates because for us stability is most important. 

* [Infrastructure maintenance](maintenance.md)
* [Stacks maintenance](../stacks/maintenance.md)

We release unplanned updates to our infrastructure for all critical security updates and notify all affected customers by email (you cannot unsubscribe from those emails).

!!! warning "Do not upgrade docker"
    When performing manual upgrade DO NOT update docker because we require a specific version of Docker, it's always behind the latest version.
