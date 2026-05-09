# Service annotations

Services can define annotations that Wodby adds to Kubernetes resources when the underlying Helm chart supports extra annotations.

Service annotations are defined under the [`annotations` section](template.md#annotations) in a service template.

Annotations are Kubernetes resource metadata. They are not the same as app endpoint route settings. Use [route settings](../apps/endpoints.md#route-settings) for HTTP routing behavior such as HTTPS redirects, no-index headers, request body size, session affinity, and path rewrites.
