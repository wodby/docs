# Organization

## Overview

Organization is a way to group all users and projects resources of your organization. It's a top level scope that consist of [projects](projects.md) and [teams](teams.md). The actual resources, such as apps and kubernetes clusters, are accessed through projects to which you can assign teams. 

Organization have a name (title) and a machine name, the machine name cannot be changed and can only be made up of lowercase letters "a-z", the numbers 0-9 and the hyphen. The machine name used for technical domains of your application instances and kubernetes clusters. Also, the machine name used in the repository namespace of Wodby Registry.

### Roles

All organization members always assigned to at least one team. Organization members have one of the following roles:

- **Owners**, they have full access to all resources and billing 
- **Admins** have full access to all resources but not billing
- **Members** have access to resources in projects they assigned to

## Invitation

You can invite users by their email (registered or not). The invited user will receive a temporary link to join which is valid for 3 days. If invited user does not have a Wodby account it will be asked to create one after visiting the invite link. 

## Settings

From your organization settings page you can manage:

- Organization members
- [Projects](projects.md)
- [Teams](teams.md)
- [Environments](apps/env.md)
- Backup presets
- Review all certificates issued for your organizations applications and upload custom certificates
- Change organization title
- Change the default organization-wide [CI/CD](cicd/index.md) system ([Wodby CI](cicd/wodby-ci.md) by default)
- Change the default organization-wide container registry ([Wodby US Docker Registry](cicd/wodby-registry.md) by default)
