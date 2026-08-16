# Custom variable providers

Custom variable providers define reusable environment-variable contracts for services that Wodby does not provide in
the built-in catalog. After creating a provider, create one or more integrations from it, enter the integration values,
and attach those integrations to app services or stacks.

Custom providers support the `variable` integration type only. They cannot define OAuth flows, account scopes,
permission audits, or infrastructure resources.

## Choose a creation method

| Method | Use when |
| --- | --- |
| Quick create | You want to define a small set of environment variables in the dashboard. |
| From manifest | You have a local `provider.yml` and do not need Wodby to track a Git repository. |
| Import from Git | You want Git to remain the source of truth, use automatic updates, or keep several providers in one repository. |

All three methods let you select organization or project ownership. An organization-owned provider can be shared with
projects in the same organization from its `Sharing` tab.

## Names and namespaces

The manifest `name` is a local slug such as `payments`. Wodby namespaces custom provider machine names with the owning
organization, producing a full name such as `acme/payments`. This lets different organizations use the same local slug
without colliding.

Use the full namespaced name when a workflow asks for the provider machine name. The manifest itself keeps the local
slug. Existing custom providers also appear under their organization namespace.

## Quick create

Use quick create when you do not need to write a manifest first:

1. Open `Providers`.
2. Select `Quick create`.
3. Select the owner and enter the provider name and title.
4. Add the fields and environment-variable names that integrations should expose.
5. Create the provider.

Open the created provider to review its generated manifest. Later updates use the same versioned manifest workflow as
providers created from a local manifest.

## Create from a manifest

1. Open `Providers`.
2. Select `From manifest`.
3. Select the organization or project that should own the provider.
4. Paste the YAML manifest, or read it from a local `.yml` or `.yaml` file.
5. Create the provider.

A minimal manifest looks like this:

```yaml
name: acme-api
title: Acme API
icon: variable
version: 1.0.0

kinds:
  - name: credentials
    title: Acme API credentials
    type: variable
    fields:
      - type: secret
        name: api_token
        label: API token
        variable: ACME_API_TOKEN
      - type: select
        name: region
        label: Region
        variable: ACME_REGION
        optional: true
        options:
          - us
          - eu
```

### Manifest fields

The top-level manifest supports:

| Field | Required | Description |
| --- | --- | --- |
| `name` | Yes | Local machine-name slug using lowercase letters, numbers, and hyphens. |
| `title` | Yes | Display name shown in the dashboard. |
| `icon` | Yes | Provider icon identifier. Use `variable` for the generic variable-provider icon. |
| `version` | Yes | Strict semantic version in `major.minor.patch` form, such as `1.2.0`. |
| `instructions` | No | Setup guidance shown when users configure an integration. |
| `fields` | No | Fields shared by every kind in the provider. |
| `kinds` | Yes | One or more variable integration kinds. |

Each kind requires `name`, `title`, and `type: variable`. A kind can also define its own `fields`, searchable `labels`,
and named `options` with optional version lists.

Each field requires:

- `type`: `text`, `secret`, `textarea_upload`, or `select`
- `name`: a unique lowercase field name
- `label`: the user-facing label
- `variable`: the environment variable exposed by the integration

Optional field properties include `description`, `optional`, `regex`, and `editable`. A `select` field must provide a
non-empty `options` list. A `textarea_upload` field can use `accept` to limit the files offered by the file picker.

Field names and environment-variable names must be unique across the complete manifest. At least one field must be
defined, either at provider or kind level. The standard
[environment-variable naming and reserved-name rules](../apps/environment-variables.md#names-and-reserved-variables)
apply. Each manifest is limited to 1 MiB.

Unknown manifest properties, duplicate YAML keys, and YAML aliases are rejected. This keeps the stored manifest
unambiguous and prevents unsupported provider capabilities from being enabled accidentally.

## Import from Git

Connect a [Git provider integration](git.md) before importing a provider from a repository.

For one provider, place `provider.yml` at the repository root. For several providers, place `index.yml` at the root and
list the relative directory for each provider:

```yaml
providers:
  - providers/acme-api
  - providers/monitoring
```

The corresponding repository layout is:

```text
index.yml
providers/
  acme-api/
    provider.yml
  monitoring/
    provider.yml
```

An index can contain up to 100 providers. Paths must be unique, relative to the repository root, and must not traverse
outside the repository.

To import:

1. Open `Providers`.
2. Select `Import from Git`.
3. Select the owner, Git integration, repository, ref type, and branch or tag.
4. Configure automatic update settings if required.
5. Select `Import` and review the task log.

Wodby imports every new provider listed by the repository. A provider whose namespaced machine name already exists is
skipped and reported in the import task.

## Update a provider

Provider updates create a new revision. Open the provider's `Manifest` tab to see the current source and version, and
use `Tasks` to review import and update logs.

### Update from a local manifest

For a provider created without Git, open `Edit`, update or upload the manifest under `Manual update from manifest`, and
select `Update`.

### Update from Git

For a Git-backed provider, open `Operations`, select the branch or tag under `Manual update from Git`, and select
`Update`.

If the repository is also used by other providers, services, or stacks, the form shows those usages. Changing the
tracked ref can update all resources using that repository together. When changing the ref, select the option to update
all shared usages so they remain aligned. The tracked ref and Git auto-update settings belong to the repository
connection, so changing them from one resource also changes them for the other resources that share it.

### Version and compatibility rules

- Keep the manifest `name` unchanged.
- Increase `version` whenever the manifest content changes.
- Versions cannot move backwards, and changed content cannot reuse the current version.
- If integrations already use the provider, an update must preserve the credential contract: kind names and options,
  field names and types, environment-variable mappings, validation, optionality, and upload constraints.
- Metadata-only changes, such as titles, instructions, and icons, can update existing integrations to the new provider
  revision automatically.

Make a credential-contract change before creating integrations, or create a separate provider contract and move
integrations deliberately.

## Automatic updates from Git

Git-backed providers can update when a supported Git integration receives a matching push event:

- a tracked branch updates when that same branch receives a push
- a tracked semantic-version tag can follow newer tags, limited to patch, minor, or major changes
- commit-pinned sources cannot use automatic updates

Configure this under `Operations > Git auto update settings`. Automatic updates use the same manifest validation,
version, and compatibility rules as manual updates. A rejected update leaves the current provider revision active; open
the provider's `Tasks` tab to review the error.

## Sharing and deletion

Use the provider's `Sharing` tab to make it available to additional projects in the same organization. Sharing a
provider does not copy integration credentials; integrations created from it keep their own ownership and sharing
settings.

A provider cannot be deleted while integrations still use it. For Git-backed providers, deleting one provider does not
disconnect a repository that is still used by another provider, service, or stack.

## Related pages

- [Variable providers](variable.md)
- [Variable integrations](../integrations/variable.md)
- [Provider vs integration](../integrations/providers-vs-integrations.md)
- [Git providers](git.md)
- [Sharing](../sharing.md)
