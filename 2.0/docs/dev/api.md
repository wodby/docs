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
- app routes
- environments

Example:

```bash
export WODBY_API_KEY=...

curl -sS \
  -H "X-API-KEY: ${WODBY_API_KEY}" \
  "https://api.wodby.com/v1/orgs"
```

REST errors are returned as regular JSON responses with an HTTP status code and a `message` field.

## Limits

Wodby applies request limits to keep the API stable for all users. Current limits may change as the platform evolves.

| Area | Limit |
| --- | --- |
| REST request body | `10 MB` |
| REST rate limit | `120` requests per second per IP, with a burst of `240` |
| GraphQL page size | Maximum `100` items per page |
| GraphQL parser size | Maximum `15000` parser tokens |
| GraphQL depth | Maximum depth `12` |
| GraphQL complexity | Maximum complexity `1000` |

Requests that exceed body-size limits can return `413 Request Entity Too Large`. Requests that exceed rate limits can return `429 Too Many Requests`.

GraphQL clients should paginate large result sets instead of requesting page sizes above `100`. GraphQL validation errors are returned as GraphQL errors. Some authentication-related GraphQL operations have additional abuse-protection throttling and can return a `RATE_LIMITED` error code.

## Practical use

Use the REST API when you want to:

- work with predictable resource URLs
- generate a client from OpenAPI
- script workflows already exposed under `/v1/...`

## Related pages

- [API keys](api-keys.md)
- [Wodby CLI](cli.md)
- [User API keys](../user/api-keys.md)
