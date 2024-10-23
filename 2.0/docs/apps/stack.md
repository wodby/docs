# Application stack

Every application has a stack. Stack is like a blueprint from which application created. All app instances of the same app have the same stack but may have different revisions. Our intended use case for a stack is to have a stack per every app unless you have many simple very similar apps in which case it might be reasonable to just have one stack. The idea is to store all configuration in a stack and when configuration changed and a new stack revisions issued (every time a stack changed we release a new revision), upgrade app instance's stacks instance by instance. This way, all of your instances can be in sync.     

## Upgrade

When a new revision of stack available you can upgrade app instance's stack. By default, we try to be less destructive with upgrades and instead provide options for you configure how exactly to perform the upgrade because some stack upgrades may have very drastic changes such as disabling or removal of app services that already in use or change linked services.

If app instance has buildable app services the upgrade will trigger rebuild of such app services because every build associated with a certain stack revision.

We always upgrade to the latest stack revision.

### Update versions to default

By default, we always keep the same options (versions) in app services during upgrade but in case of, let's say, when you want to update all instances from end-of-life versions to new one, you can check this option, and we will override the versions. 

### Update replicas

When checked we will set replicas number in all app services to the one set in the latest stack revision.

### Override resources

When checked we will set resources request and limits in all app services to the one set in the latest stack revision.

### Override integrations

When checked we will override linked integrations in all app services to the one set in the latest stack revision.

### Override enabled services

When checked we will enable or disabled app services as they are in the latest stack revision.

### Override service settings

When checked we will override values of all settings to the values in the latest stack revision.

### Override links

When checked we will relink all services to how they are in the latest stack revision.

### Override tokens

When checked we will override values of all tokens to the values in the latest stack revision.

### Override configs

When checked we will override configs to those that are in the latest stack revision.

### Override cron schedules

When checked we will override cron schedules to those that are in the latest stack revision.

### Override main app service

When checked we will override main app service to the one in the latest stack revision. This may result in creating a new domain (main technical domain will be reattached), re-issuing a certificate, hence a certain downtime.
