# Organization settings

Organization owners and administrators can open `Organization > Settings > Builds` to configure the default retention period for unused CI build images.

## Build image retention

Choose **Auto-void images of unused builds for all apps older than**, then click **Save**. The available values are **Never**, **1 month**, **3 months**, **6 months**, and **1 year**. The initial default is **Never**, which disables automatic cleanup.

New app instances inherit this default. Changing it also updates existing instances whose setting matches the previous organization default; instances with a different setting keep their override. To change one instance independently, use `Instance > Builds > Settings > Auto-clean images`.

Retention is measured from the build's original creation date. Enabling or shortening it can make older unused builds eligible for cleanup immediately. Cleanup runs in the background and protects images used by any instance's current build.

Build history remains after cleanup, but a build cannot be deployed again once its required images have been removed. External registry images are not deleted by this setting.

See [Build image cleanup](../apps/deploy.md#automatically-clean-unused-build-images) for details and manual cleanup, and [Container registry storage](../billing.md#container-registry-storage) for billing.
