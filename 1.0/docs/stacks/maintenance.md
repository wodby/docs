# Stacks maintenance

We regularly update stacks by releasing new versions, such updates can include security updates and performance improvements. You can find more details under the Changelog tab on a stack page.

!!! tldr "Stacks and infrastructure maintained separately"
    For infrastructure maintenance see [this article](../infrastructure/maintenance.md) 

The stack has a requirement for the minimal version of infrastructure of the server where this stack is deployed. You can find a stack's version of your application on the list of your apps or under Stack tab of your instance. If a stack is outdated you will see an appropriate indicator.
​
![](../assets/stack-upgrade.png)​
​
## Updating organization stack

When a new version of a stack has been released your stack will be marked as outdated. You can update a stack to the latest version from a stack page in your organization. This update will not affect your applications, it only updates the version of a stack inside of your organization.

## Upgrading application stack

!!! warning "Review stack changelog"
    Before performing the upgrade make sure to read the stack's changelog. Pay attention to "Upgrade instructions". Be especially attentive you perform major versions upgrade (e.g. `4.x.x` to `5.x.x`).

Once you update a stack in your organization, you can upgrade the application instances. Go the Instance > Stack > Operations page and click Upgrade . The downtime depends on the number of services affected in a new version and what deployment strategy used in these services.
