# Wodby API

Wodby exposes a public REST API for resource-oriented automation and OpenAPI-based tooling.

## API reference

The API reference is published as a separate OpenAPI reference site, not as a MkDocs page:

- [Wodby API reference](https://wodby.com/docs/2.0/api/)
- [OpenAPI JSON](https://wodby.com/docs/2.0/api/openapi.json)
- [OpenAPI YAML](https://wodby.com/docs/2.0/api/openapi.yaml)

Use the reference site when you need endpoint details, request and response schemas, or generated model names.

## Base URL

Use `https://api.wodby.com/v1` for REST requests.

Wodby also publishes the live OpenAPI description from the API itself:

- `https://api.wodby.com/v1/openapi.json`
- `https://api.wodby.com/v1/openapi.yaml`

## Authentication

Authenticate public API requests with an [API key](api-keys.md) sent in the `X-API-KEY` header.

| Method | Header | Typical use |
| --- | --- | --- |
| API key | `X-API-KEY` | Recommended for user automation |

## Covered resources

The public REST API includes:

- users, organizations, memberships, projects, and environment definitions
- apps, app environments, app services, authentication, ports, routes, certificates, builds, and deployments
- clusters and databases
- integrations, integration kinds, providers, Git repositories, and Helm chart analysis
- service and stack catalogs, including stack services
- backups, imports, tasks, and task-step logs

Use the [API reference](https://wodby.com/docs/2.0/api/) as the source of truth for the current endpoints and schemas.

## App environment terminology

`App environment` is the canonical public name for the resource previously called an `app instance`. Public REST
clients should use `/v1/app-environments`; the public API does not expose a `/v1/app-instances` compatibility route.

Example:

```bash
export WODBY_API_KEY=...

curl -sS \
  -H "X-API-KEY: ${WODBY_API_KEY}" \
  "https://api.wodby.com/v1/orgs"
```

REST errors use `application/problem+json` and an RFC 9457-style problem-details body. Responses include `type`,
`title`, `status`, `detail`, a stable Wodby `code`, and a backward-compatible `message` alias that matches `detail`.
Validation failures can also include an `errors` array with field-specific details.

## Limits

Wodby applies request limits to keep the API stable for all users. Current limits may change as the platform evolves.

| Area | Limit |
| --- | --- |
| REST request body | `10 MB` |
| REST rate limit | `120` requests per second per IP, with a burst of `240` |

Requests that exceed body-size limits can return `413 Request Entity Too Large`. Requests that exceed rate limits can return `429 Too Many Requests`.

## Practical use

Use the REST API when you want to:

- work with predictable resource URLs
- generate a client from OpenAPI
- script workflows already exposed under `/v1/...`

Generate a client from the OpenAPI schema when you want typed models for new `/v1` integrations. Existing SDKs for the older v3 API surface are listed under [SDKs](sdks.md).

Use [Wodby MCP](mcp.md) instead when an AI assistant needs to inspect Wodby context, diagnose deployments, or run
approved Wodby operations through a tool interface.

## Related pages

- [API keys](api-keys.md)
- [Wodby MCP](mcp.md)
- [SDKs](sdks.md)
- [Wodby CLI](cli.md)
- [User API keys](../user/api-keys.md)
