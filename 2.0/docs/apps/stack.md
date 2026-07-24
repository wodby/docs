# Application stack

```mermaid
flowchart TD
    subgraph App2["<div style='margin-top:10px; white-space: nowrap;'>Your app</div>"]
        subgraph group[ ]
            Dev["Dev instance"]
            Staging["Staging instance"]
            Prod["Production Instance"]
        end
        style group fill:none,stroke:none,stroke-width:0px
    end   

    subgraph Stack["<div style='margin-top:10px; margin-right: 60px; white-space: nowrap;'>App stack</div>"]
        subgraph group3[ ]
            Rev1["Revision #1"]
            Rev2["Revision #2"]
        end
        style group3 fill:none,stroke:none,stroke-width:0px            
    end
    
    Dev --> Rev1
    Staging --> Rev2
    Prod --> Rev2
```

Every application is built from a stack.

Think of a stack as the blueprint for the app:

- it defines the services the app uses
- it defines default configuration for those services
- each published stack change produces a new stack revision

All [app instances](instances.md) of the same app share the same stack, but they can run different stack revisions.

The usual model is one stack per application. When the stack changes, you upgrade instances revision by revision so environments can move forward at their own pace.

## Upgrade

When a new published stack revision is available, you can upgrade an app instance to it. Unpublished stack drafts are
not available for app upgrades and do not mark app instances as outdated.

Open `Apps`, select the app, select an app instance, and go to `Stack > Operations`. The `App instance stack` table
shows the current stack revision, stack version, and status. The status is `Outdated` when a newer stack revision is
available and `Up to date` when the instance already uses the latest revision.

The `Upgrade stack` form is on the same subtab. The `Upgrade` button is enabled only when the app instance is outdated.
If the instance already uses the latest stack revision, the button says `Stack is up to date`.

Wodby does not force every possible override during upgrade. Instead, the upgrade flow lets you decide which parts of the latest stack revision should replace the current app-instance overrides.

The reason is that app services can be customized per instance. Wodby cannot always tell whether an app-level value was
changed intentionally or whether it simply has not received a newer stack default yet.

If the app instance has services with build sources, the upgrade triggers rebuilds for those services because builds are tied to a specific stack revision.

The dashboard always upgrades to the latest stack revision. There is no revision selector in the upgrade form.

All upgrade options are disabled by default. `Update versions to default` and `Update replicas` are shown directly in
the form. The remaining options are under `Advanced settings`.

## Auto-upgrade

An app instance can be configured to upgrade its stack automatically after the stack is automatically updated.
This is an app-instance setting, so production, staging, and development instances can use different behavior even when
they belong to the same app.

Auto-upgrade uses the same settings as the manual `Upgrade stack` form. The saved settings decide which app-instance
overrides Wodby replaces with values from the latest stack revision.

Auto-upgrade can run after supported automatic stack updates, including Git-backed stack auto-updates, automatic stack
service revision updates, and automatic sync with origin.

Auto-upgrade is disabled by default. Enable it only for instances where it is acceptable to move to the latest stack
revision without a manual review step. If the stack upgrade creates app services that need extra configuration, Wodby
records warnings and waits for you to finish the service configuration before deployment, the same as a manual stack
upgrade.

Manual stack updates, manual syncs, and manually published drafts do not force app instances forward. Use the manual
upgrade flow when you want to control the rollout yourself.

During upgrade, Wodby matches existing app services to stack services by stack service name.

- If a matching stack service still exists, the app service is moved to the new stack revision and the upgrade settings below decide which app-level values are replaced.
- If a stack service was added, Wodby creates the missing app service during the upgrade.
- If a stack service was removed, the obsolete app service is marked for deletion and its Kubernetes resources are uninstalled after the upgrade task.

Service revision, title, type, icon, and required status are updated to match the new stack service. Required services
are kept enabled even if the stack service is disabled.

The upgrade task logs the changes it applies and also logs when it detects a stack change but skips it because the
corresponding upgrade setting is disabled.

New app services may need app-specific configuration that cannot be selected safely at stack-upgrade time, such as a
build source, an external database, required integrations, or required settings. These gaps do not stop the
stack upgrade. Wodby records them as warnings on the upgrade task, creates the app service, and waits for you to finish
the service configuration before deploying.

If a newly added service supports build boilerplates, Wodby uses the default build boilerplate automatically. If no
boilerplate is marked as default, the first boilerplate is used. If the default boilerplate cannot be applied, Wodby
records a warning and asks you to select the build source after the upgrade.

When a stack upgrade leaves unresolved service configuration, Wodby skips the automatic post-upgrade deployment.
Deployments are blocked until the app instance reports complete service configuration.

### Update versions to default

By default, Wodby keeps existing app-service versions during upgrade. Enable this option when you want top-level app
services to move to the default versions defined by the latest stack revision.

This does not stop the app service from moving to the latest service revision used by the stack. It controls the
app-service version option, such as the PHP, MariaDB, or Redis version selected for that service.

Use this when the latest stack revision changes an app service from an EOL default version to a supported default
version. If you want to choose a different supported version, upgrade the stack first and then edit the app service from
`Stack > App services`.

### Update replicas

When enabled, Wodby updates app-service replica counts to match the latest stack revision.

Replicas are not applied to app services that remain disabled. If the same upgrade also enables a service through
`Override enabled services`, replicas are applied after the service is enabled.

### Override resources

When enabled, Wodby updates resource requests and limits to the values from the latest stack revision.

If disabled, existing app-level resource values are kept. Resource records for stack-defined containers can still be
created when they did not exist before.

### Override integrations

When enabled, Wodby creates integrations defined by the latest stack revision and removes app-service integrations that
are no longer defined by the stack service.

If disabled, existing app-service integration selections are kept.

### Override enabled services

When enabled, Wodby aligns enabled and disabled services with the latest stack revision.

If disabled, existing app-service enabled or disabled state is kept for services that still exist in the stack. This
option does not keep obsolete app services when their stack service was removed.

### Override service settings

When enabled, Wodby replaces service-setting values with the latest stack defaults.

New settings introduced by the service revision are created during upgrade. If disabled, existing app-level setting
values are kept unless the setting changes from a direct value to a linked value or back.

### Override links

When enabled, Wodby updates service links to the latest stack configuration and deletes app-service links that no longer
exist in the stack service.

If disabled, existing link targets and extra app-service links are kept. Missing links from the new stack are still
created so newly introduced required connections can work.

### Override tokens

When enabled, Wodby recreates app-service tokens from the latest service and stack definitions.

When the same token name and environment type is defined in multiple places, Wodby applies service-defined tokens first,
then stack-wide tokens, then stack-service tokens.

If disabled, tokens are left unchanged. This avoids replacing secrets that may have been intentionally customized for
one app instance.

### Override configs

When enabled, Wodby replaces app-service config overrides with the latest stack configuration.

New configs introduced by the service revision are created when the stack provides an override. Existing config
overrides are kept when this setting is disabled.

### Override cron schedules

When enabled, Wodby updates cron schedules to match the latest service and stack configuration.

New cron schedules introduced by the service or stack are created during upgrade. Existing cron schedules are kept when
this setting is disabled.

### Override volumes

This option is shown in the dashboard as `Override volumes (may cause data loss)`.

When enabled, Wodby deletes app-service volume records that no longer exist in the latest service manifest.

New volumes introduced by the service revision are created during upgrade. Existing volume sizes are not changed for
running app instances.

### Override main app service

When enabled, Wodby changes the main app service to match the latest stack revision. This can trigger route reassignment, certificate re-issuance, and possible downtime.

If the current main app service was removed from the stack, Wodby updates the main service even when this option is not
selected, because the old main service can no longer stay active.

## Related pages

- [Applications overview](index.md)
- [Instances](instances.md)
- [App services](services.md)
- [Stack updates](../stacks/updates.md)
