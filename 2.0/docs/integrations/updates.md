# Integration provider updates

Providers can change after you create an integration. Wodby publishes each provider change as a new revision. A
compatible managed-provider rollout can advance integrations automatically; otherwise, an existing integration stays
on the revision it was configured against. Revision pinning prevents an incompatible provider update from silently
changing how existing credentials, selected kinds, or environment variables are interpreted.

New integrations use the provider's current revision. Existing integrations continue working with their pinned
revision until you update them explicitly.

For a custom provider, including a Git-backed provider, manual and automatic provider updates publish a new revision
without changing existing integrations.

## Find outdated integrations

An integration is **Outdated** when its pinned provider revision is older than the provider's current revision. The
dashboard shows an **Outdated** label in the `Integrations` list.

Open the integration to compare its current and target provider revisions. Users with `Modify/Delete` access can also
see whether Wodby can update the integration safely.

An outdated integration is not automatically broken or disabled. It continues using its pinned provider revision.

## Update an integration

To update an integration:

1. Open `Integrations` and select an integration marked **Outdated**.
2. Review the current and target revisions in the provider update notice.
3. Review any compatibility reasons shown by Wodby.
4. If the update is compatible, select `Update provider`.
5. If every incompatibility comes from fields removed by the new provider revision, select
   `Drop fields and update`, review the fields, and confirm the permanent deletion.

Wodby checks compatibility again when you submit the update. A successful update changes the integration's provider
revision and related selected-kind metadata together. A confirmed destructive update also deletes the listed stored
field values and any secrets owned by those fields in the same operation. Variables exported by those fields stop
being available to resources that use the integration. Wodby marks affected app services for redeploy so their next
deployment uses the new variable set.

When a provider update leaves existing integrations pinned, update each compatible integration when you are ready to
adopt the new contract.

## Compatible updates

The `Update provider` action is available only when the integration's stored configuration is compatible with the
current provider revision. Wodby evaluates the actual integration, including:

- selected kinds and kind options
- authentication and scope
- stored fields and their environment-variable mappings
- field types and secret storage
- required fields and validation rules
- provider version compatibility, when the provider uses semantic versions

Additive changes do not necessarily block an update. For example, adding a new kind that the integration does not use
or adding an optional field can remain compatible.

## Updates that require migration

When Wodby cannot preserve the existing integration contract safely, the dashboard shows the compatibility reasons.
If deleting fields absent from the target revision resolves every reason, Wodby offers `Drop fields and update`. This
action requires confirmation because the listed values and secrets cannot be recovered through the integration.

Wodby does not offer the destructive action for unrelated contract changes. The integration stays pinned when another
migration is required. Examples include:

- removing a selected kind or required capability
- removing a field for which the integration has a stored value
- adding a required field without a stored value
- changing a field's environment-variable name, type, or secret classification
- changing authentication or scope in a way that does not match the integration
- adding validation that rejects the stored value
- moving to an incompatible major provider version

The provider's new revision remains available to new integrations. Existing integrations with unsupported changes
require a provider-specific migration or a replacement integration before they can leave the older revision.

## Shared OAuth integrations

An OAuth integration shared with another organization has one canonical source integration and one or more receiving
organization handles. The source owner controls provider revision updates. Wodby updates the source and all handles as
one operation so they cannot interpret the shared credentials using different provider revisions.

A receiving organization can see that its handle is outdated, but it cannot initiate the update. Ask the source
organization owner to update the canonical integration.

## Related pages

- [Integrations overview](index.md)
- [Provider vs integration](providers-vs-integrations.md)
- [Organization sharing](organization-sharing.md)
- [Providers overview](../providers/index.md)
- [Custom variable providers](../providers/custom-variable-providers.md)
