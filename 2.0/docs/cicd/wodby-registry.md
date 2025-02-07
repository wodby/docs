# Wodby Registry

Wodby Registry is a private Docker registry that is used to store your application images. It is located in the US region and is available at `us-docker.wodby.com`.

You can authenticate to Wodby Registry using your Wodby account credentials.

## Repositories

We create a new repository per each application instances, available as `[org-name]/[app-name]-[app-instance-name]`.

!!! important
    Docker images that are not associated with existing application instances and builds will be automatically cleaned up.
