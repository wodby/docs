# Docker Hub

Docker Hub is available in Wodby as a `registry` provider. Use it when you want Wodby to authenticate against an external Docker Hub registry for image push and pull operations.

## Setup fields

| Field | Required | Notes |
| --- | --- | --- |
| Namespace | No | Docker Hub user or organization namespace for pushed images. If empty, Wodby uses the push/pull username. |
| Username (push/pull) | Yes | Account used for push and pull access |
| Access Token (push/pull) | Yes | Token paired with the main username |
| Username (pull only) | No | Optional separate account for pull-only access |
| Access Token (pull only) | No | Optional token for the pull-only account |

## Usage

Create a Docker Hub integration and select it as the registry when creating an app or app instance with buildable services.

Wodby publishes build images to Docker Hub under a repository path based on the app instance:

```text
[namespace]/[app-name]_[app-instance-name]-[suffix]
```

The namespace is the optional `Namespace` field. If you leave it empty, Wodby uses the main Docker Hub username as the namespace.

Use the main username and access token for image publishing. Make sure this account can push to the selected namespace.

If you use only one Docker Hub account for both push and pull, fill only the main credentials. Use the pull-only credentials when runtime deployments should pull images with a different account from the account that publishes images. Wodby uses pull-only credentials for deployment image pulls only when both pull-only fields are set; otherwise it falls back to the main credentials.
