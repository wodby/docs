# Kubernetes cluster updates

## Infrastructure updates

[Infrastructure apps](infrastructure.md) that we deploy work the same way as usual apps, i.e. they have a stack and a version. So when we release an update to a service, a new infrastructure stack version will be released and your cluster will be marked as outdated. You can then manually upgrade app stack of infrastructure apps. 

Auto-updates are not currently available.

## Worker node updates

For [managed kubernetes](managed.md) clusters the simplest way of "updating" nodes is by recycling them.

## Kubernetes version updates

Coming soon...
