# Distribution Registry

Distribution Registry is available in Wodby as a `registry` provider. Use it to connect a self-hosted registry that is compatible with Docker Distribution.

## Setup fields

| Field | Required | Notes |
| --- | --- | --- |
| Host | Yes | Registry hostname. You can enter `registry.example.com`, `registry.example.com:5000`, or a URL with `http://` or `https://`. Wodby stores and uses the normalized host without a scheme in image names. |
| Repository prefix | No | Prefix for repositories created by Wodby, for example `team/apps`. If empty, Wodby uses the organization machine name. |
| Username (push/pull) | Yes | Account used for push and pull access |
| Password (push/pull) | Yes | Password or access token paired with the main username |
| Username (pull only) | No | Optional separate account for deployment image pulls |
| Password (pull only) | No | Optional password or token for the pull-only account |

## Usage

Create a Distribution Registry integration and select it as the registry when creating an app or app instance with buildable services.

Wodby publishes build images under a repository path based on the configured prefix and app instance:

```text
[prefix]/[app-name]_[app-instance-name]-[suffix]
```

If `Repository prefix` is empty, Wodby uses your organization machine name as the prefix.

Use the main username and password for image publishing. Make sure this account can push to repositories under the configured prefix.

If you use only one registry account for both push and pull, fill only the main credentials. Use the pull-only credentials when runtime deployments should pull images with a different account from the account that publishes images. Wodby uses pull-only credentials for deployment image pulls only when both pull-only fields are set; otherwise it falls back to the main credentials.

When you create or update a Distribution Registry integration, Wodby follows the Docker Registry v2 authentication challenge returned by the registry. For token-based registries, Wodby requests a token for a temporary permission-check repository under the configured prefix and verifies the requested push or pull scope. The registry still enforces access again when builds push images and deployments pull them.
