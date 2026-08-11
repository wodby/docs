# Database users

From `Databases > [Database] > Users` you can create database users.

When creating a user, specify:

- username
- password
- which DBs the user should have access to

From `Databases > [Database] > Users > [User]` you can:

- review the user's current status
- reveal the current password on demand
- change which DBs the user can access
- delete the user

Revealing the current password requires
[runtime secret reveal permission](../access-control.md#secret-reveal-permissions) and recent password confirmation.

For container-based app databases, Wodby usually creates an app-specific user automatically based on the service's `database` configuration.

User creation is safe to retry. If a same-named database account already exists and accepts the requested password,
Wodby keeps it and continues applying the selected database grants. If the account exists with different credentials,
Wodby reports an error instead of deleting the account, changing its password, or taking ownership of it.
