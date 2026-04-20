# SSH services

SSH services use the `ssh` type.

They are usually defined as [derivatives](derivatives.md) of another service so they inherit the parent service's
versions, environment variables, and related configuration while exposing SSH access separately.

Use this type when you need shell or file-access workflows around an existing application service.
