Source: https://wodby.com/docs/2.0/databases/users/

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

Creating, changing, and deleting users requires permission to modify the database. For a database that belongs to an
app environment, it also requires the `Configure` [permission](https://wodby.com/docs/2.0/access-control/#environment-permissions) in that
environment type.

Revealing the current password requires
[runtime secret reveal permission](https://wodby.com/docs/2.0/access-control/#secret-reveal-permissions) and recent
[secret reveal confirmation](https://wodby.com/docs/2.0/user/security/#secret-reveal-confirmation).

For container-based app databases, Wodby usually creates an app-specific user automatically based on the service's `database` configuration.

User creation is safe to retry. If a same-named database account already exists and accepts the requested password,
Wodby keeps it and continues applying the selected database grants. If the account exists with different credentials,
Wodby reports an error instead of deleting the account, changing its password, or taking ownership of it.
