# Docker Hub

Docker Hub is available in Wodby as a `registry` provider. Use it when you want Wodby to authenticate against an external Docker Hub registry for image push and pull operations.

## Setup fields

| Field | Required | Notes |
| --- | --- | --- |
| Username (push/pull) | Yes | Account used for push and pull access |
| Access Token (push/pull) | Yes | Token paired with the main username |
| Username (pull only) | No | Optional separate account for pull-only access |
| Access Token (pull only) | No | Optional token for the pull-only account |

## Usage

If you use only one Docker Hub account for both push and pull, fill only the main credentials. Use the pull-only credentials when you want runtime pulls to use a different account from image publishing.
