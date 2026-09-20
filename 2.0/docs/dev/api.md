# Wodby API

Wodby exposes a public REST API for resource-oriented automation and OpenAPI-based tooling.

## API reference

Use the API reference for endpoints and request and response schemas:

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

## Cluster capability policy

!!! warning "Policy storage only"

    The cluster settings contract includes `clusterCapabilities`, but automatic operator installation and deployment
    dependency enforcement are not available yet. Saving `autoInstall: true` does not install operators or make a
    capability-dependent application ready to deploy. Leave it disabled for normal use.

The REST `clusterCapabilities` object contains:

- `autoInstall`: required boolean when submitting the object; disabled by default.
- `stackRevisionIds`: required array of up to 128 unique, positive integer IDs identifying approved, published stack
  revisions. These are revision IDs, not stack IDs.

Omitting `clusterCapabilities` preserves the existing policy. If the object is supplied, both fields must be present
and non-null. An explicit empty array clears the approved revisions; an explicit `false` disables the flag.

New approvals must reference revisions the caller can access. Private stacks must match the cluster's organization
and ownership scope. Enabling the flag revalidates all retained approvals. Disabling it or removing stale approvals
does not require renewed access to those revisions.

GraphQL uses `stackRevisionIDs` with string-valued IDs. MCP update input uses
`cluster_capabilities.auto_install` and `cluster_capabilities.stack_revision_ids`; its output uses the REST-style
`clusterCapabilities`, `autoInstall`, and `stackRevisionIds` names.

For service authors, see the [cluster capability declaration reference](../services/template.md#clustercapabilities).

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
