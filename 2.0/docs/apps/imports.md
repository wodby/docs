# Application Imports

If an application's stack includes services that provide [import functionality](../services/operations.md#imports), you can run imports for the corresponding app service.

There are two main import methods.

## 1. Simple files import

Wodby imports files directly into the running volume by unpacking the provided tar archive to the specified path.

This method is not transactional.

## 2. Through init volume

Wodby mounts the import archive into the init volume provided by the service, and a container performs the import during startup. This pattern is commonly used for databases.

This method is transactional. Wodby starts a copy of the app service with a new persistent volume. If the import succeeds, Wodby redeploys the service using the new volume that contains the imported data.

For a container-based database service, Wodby provisions the app's database user on the replacement volume and
reapplies its managed database grants before redeployment. A missing user is created, and an existing user is accepted
when it already uses the expected credentials. If an uploaded dump creates a same-named user or role with different
credentials, the import task reports a credential conflict instead of replacing that account. Database dumps intended
for this workflow should normally contain the application database schema and data, not server-level user or role
definitions.

## K3S storage capacity preflight

Before an app-service import runs on K3S, its task checks the capacity of the destination volume.

For a transactional init-volume import using the default local-path provisioner, Wodby accounts for the replacement
data volume and the temporary 10 GiB import volume while the current volume still exists. The import stops before
creating replacement claims when known available capacity is insufficient or the backing node reports
`DiskPressure`.

For an in-place files import, the service contract does not declare the incoming archive's expanded size. Wodby still
checks disk pressure, but reports byte capacity as unverified and continues. The same warning behavior applies when
Kubernetes volume statistics or a provisioner-specific capacity resolver are unavailable.

When the import source is a pending app-service backup, Wodby checks the destination before creating that backup,
checks the source backup volume through its own preflight, and checks the destination again before import
provisioning. Storage operations are serialized for every involved K3S cluster.

External database imports do not use this Kubernetes volume preflight.
