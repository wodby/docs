# Teams

Teams are reusable groups of organization members.

Use teams when several people should receive the same project access repeatedly. Instead of adding every user to every project one by one, you can add the team once and manage membership inside the team.

## Team roles

Teams have two roles:

- `Member`
- `Team leader`

Team leaders can view and update the teams they lead. Organization owners and admins can manage all teams, and only they can delete teams.

## How teams are used

Teams do not replace [project access](access-control.md). Instead, they help you assign project access at scale.

Typical workflow:

1. Create a team such as `Developers`, `Support`, or `Marketing`.
2. Add organization members to that team.
3. Add the team to one or more [projects](projects.md).
4. Choose the appropriate project role for that team, such as `Read`, `Write`, or `Admin`.

A user can belong to multiple teams, and those teams can be added to different projects.

## Teams and direct access

Projects can also grant access directly to individual organization members. You do not have to use teams for every case.

If a user receives project access both directly and through one or more teams, Wodby applies the highest project role available to that user in that project.

## When to use teams

Teams work best when:

- the same group needs access to many projects
- you want one place to manage membership for a department or function
- you want to keep direct project memberships limited to exceptions

Use direct project membership when access is specific to one person rather than a reusable group.

## Related pages

- [Projects](projects.md)
- [Access control](access-control.md)
