# Container registry integration

Add a container registry integration when a stack references images from a
private registry. The integration belongs to the organization and supplies an
image-pull secret to matching services during deployment.

## Configure the integration

Open `Organization > Integrations`, select the custom container registry
provider, and enter:

- the registry hostname, without a repository path;
- the registry username; and
- a password or access token with pull permission.

The configured hostname must exactly match the registry host parsed from the
service image. For example, an image named
`registry.example.com/team/application:release` matches a registry integration
whose host is `registry.example.com`. Docker Hub images and images in another
hostname require the corresponding integration.

Wodby encrypts the credential and renders it into a Kubernetes/Docker image
pull secret for the deployment. It does not add the credential to the
container's environment.

## Apply and rotate credentials

Redeploy affected instances after adding, replacing, or removing registry
credentials so their rendered pull secrets and workloads use the current
integration.

For rotation:

1. Create the new pull-only token at the registry.
2. Update the Wodby integration.
3. Redeploy every affected instance and confirm that its images can be pulled.
4. Revoke the previous token at the registry.

If Wodby cannot decrypt a stored credential, deployment fails rather than
silently deploying without the required pull secret. Re-enter the registry
credential and retry after confirming the previous deployment's state.

Organization administrators and owners can manage registry integrations. See
[Permissions](../roles.md#organization-permissions).

This integration is for pulling service images from an external registry. CI
images stored in `registry.wodby.com`, their retention, and their billing are
described under [Code deployment](../apps/deploy.md#automatically-clean-unused-build-images)
and [Container registry storage](../billing.md#container-registry-storage).
