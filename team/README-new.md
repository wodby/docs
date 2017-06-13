# Team Management

## Global Roles

By default Wodby provides only two roles: Owners and Administrators, both have full access to organization's resources. The only difference is that Administrators can't access billing. Owner role designed for CxO (especially CTO, CIO), Administrator role designed for system administrators, Ops, DevOps, Head/VP of Engineering, in other words, for guys who is responsible for servers and infrastructure in your organization.

## Access Control

In Wodby, access control is based on two main concepts – teams and resources. Available resources:

* [Applications](../apps/README.md) and [instances](../apps/instances.md)
* [Integrations](../integrations/README.md)
* [Repositories](../git/README.md)
* [Servers](../servers/README.md)
* [Stacks](../stacks/README.md)

Every resource is assigned to a team that can be created by Administrators. There are two roles in every team - Team Leaders and Team Members. Team Members can create and access all resources assigned to their team except servers and application instances with type Production, such resources are available only for Team Leaders. Team Leaders are managed by Administrators, Team Members are managed by Team Leaders. 

A typical use case:

1. Administrator connects servers to Wodby, marks one of them as production
2. Administrator creates a team and assign a leader
3. Team leader adds members to his team 
4. Team members create all required resources to start building an application
5. When the application is ready, team leader deploys a production instance to a production server (available only for him)