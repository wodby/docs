# Access control

Wodby access is layered. The same user can have:

- an organization role
- one or more team memberships
- one or more project memberships

Understanding those layers makes the dashboard behavior much easier to predict.

## Organization roles

Organization membership decides whether a user can access the organization at all.

- `Owner` has full access to resources and billing
- `Admin` has full access to resources but not billing
- `Member` works through project-level access

In practice, organization owners and admins already have full access across the organization. Project roles matter most for organization members.

## Team roles

Teams are reusable groups inside an organization. They have their own roles:

- `Member`
- `Team leader`

Team leaders can manage the teams they lead. Organization owners and admins can manage all teams, and only they can delete teams.

## Project roles

Project access is where day-to-day resource permissions are controlled.

Projects can grant access to:

- individual organization members
- teams

Project roles are:

- `Read` to view the project and its resources
- `Write` to modify resources inside the project
- `Admin` to manage the project itself

## Direct access and team access

A user can receive project access in more than one way:

- directly as an organization member added to the project
- indirectly through one or more teams added to the same project

When that happens, Wodby applies the highest project role available to that user in that project.

Example:

- the user is added directly with `Read`
- one of their teams is added with `Write`
- effective access becomes `Write`

## Where project access is managed

Manage project access from `Organization > Projects > [Project] > Access`.

From there you can:

- see current memberships
- add organization members
- add teams
- assign `Read`, `Write`, or `Admin`
- change roles later
- remove project memberships

## How this affects resources

Project roles apply only inside that project.

- `Read` users can see resources
- `Write` users can change resources that belong to the project
- `Admin` users can manage the project itself

Separate [sharing](sharing.md) rules still apply for resources shared from other projects. If a resource is shared as read-only, it stays read-only in the target project even for project admins.

## Boundaries

Projects are isolation boundaries as well as permission boundaries.

- Resources are not automatically available across projects.
- Cross-project references do not work unless the required resource is explicitly shared.
- Deleting a project requires removing the resources that still belong to it.

## Related pages

- [Organization](org.md)
- [Projects](projects.md)
- [Teams](teams.md)
- [Sharing](sharing.md)
