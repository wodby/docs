# Service imports

Service can define data imports. There are two types of how imports performed:

## 1. Simple files import

In this case we run import directly in the running volume by unpacking a provided tarball to a specified path. It's not transactional.

## 2. Through init volume

In this case we mount the import archive to the init volume provided by the service, a container will perform the import from the init volume during a start-up. Normally used for databases.

This import is transactional. We spin up a copy of the app service with a new persistent volume, if the import successful we perform a service redeploy during which a new persistent volume with the imported files mounted.
