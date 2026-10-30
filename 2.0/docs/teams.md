# Teams

Teams are reusable groups of organization members.

Use teams when several people should receive the same project access repeatedly. Instead of adding every user to every project one by one, you can add the team once and manage membership inside the team.

## Team roles

Teams have two roles:

- `Member`
- `Team leader`

Team leaders can see the teams they lead and their members. Organization owners and admins can create, update, and delete teams, including team membership and team leader changes. They can also change a person's teams from the member's page, `Organization > Members > [Member] > Teams`.

## How teams are used

Teams do not replace [project access](access-control.md). Instead, they help you assign project access at scale.

Typical workflow:

1. Create a team such as `Developers`, `Support`, or `Marketing`.
2. Add organization members to that team.
3. Add the team to one or more [projects](projects.md).
4. Choose the [project role](access-control.md#project-roles) for that team: a system role such as `Read`,
   `Developer`, or `Write`, or one of your organization's custom roles.
5. For `Write` and the `Developer` roles, choose whether team members can reveal secrets in that project.

A user can belong to multiple teams, and those teams can be added to different projects.

Teams cannot receive roles that manage the project: the system `Admin` role, or custom roles with the `Manage project`
permission. Project administration is granted directly to specific organization members.

## Teams and direct access

Projects can also grant access directly to individual organization members. You do not have to use teams for every case.

If a user receives project access both directly and through one or more teams, they get every permission that any of
those memberships grants. See [Combining access](access-control.md#combining-access).

Secret reveal is allowed when any one of those direct or team memberships allows it. See
[Secret reveal permissions](access-control.md#secret-reveal-permissions).

## When to use teams

Teams work best when:

- the same group needs access to many projects
- you want one place to manage membership for a department or function
- you want to keep direct project memberships limited to exceptions

Use direct project membership when access is specific to one person rather than a reusable group.

## Related pages

- [Projects](projects.md)
- [Access control](access-control.md)
