# Service certificates

This page covers self-signed certificates defined in service templates, not endpoint TLS certificates for application domains. For managed endpoint certificates and organization-wide certificate inventory, see [App endpoints](../apps/endpoints.md#tls-certificates).

Services can define self-signed certificates that are generated and then mounted into Kubernetes resources through Helm.

Service certificates are defined under the [`certs` section](template.md#certs) in a service template.
