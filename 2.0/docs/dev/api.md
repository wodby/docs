# Wodby API

Wodby exposes a public REST API for resource-oriented automation and OpenAPI-based tooling.

## Base URL

Use `https://api.wodby.com/v1` for REST requests.

Wodby also publishes an OpenAPI description at:

- `https://api.wodby.com/v1/openapi.json`
- `https://api.wodby.com/v1/openapi.yaml`

## Authentication

Authenticate public API requests with an [API key](api-keys.md) sent in the `X-API-KEY` header.

| Method | Header | Typical use |
| --- | --- | --- |
| API key | `X-API-KEY` | Recommended for user automation |

## Covered resources

The current REST API covers a focused subset of resources. At the time of writing, the backend exposes endpoints for:

- organizations
- projects
- apps
- app instances
- app deployments
- app builds
- clusters
- databases
- integrations
- backups
- app domains
- environments

Example:

```bash
export WODBY_API_KEY=...

curl -sS \
  -H "X-API-KEY: ${WODBY_API_KEY}" \
  "https://api.wodby.com/v1/orgs"
```

REST errors are returned as regular JSON responses with an HTTP status code and a `message` field.

## Practical use

Use the REST API when you want to:

- work with predictable resource URLs
- generate a client from OpenAPI
- script workflows already exposed under `/v1/...`

## Related pages

- [API keys](api-keys.md)
- [Wodby CLI](cli.md)
- [User API keys](../user/api-keys.md)
