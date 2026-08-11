# Share an OAuth integration with another organization

OAuth providers may allow a third-party account or installation to be connected to Wodby only once. Instead of
reconnecting or copying its credentials, an organization can invite another Wodby organization to use the existing
integration.

This is different from project sharing. Project sharing controls access inside one Wodby organization. Organization
sharing creates a separate integration in the invited organization while keeping the OAuth credentials with the
source organization.

## Requirements

An integration can be shared with another organization when it is:

- authenticated through OAuth
- in `OK` status
- a canonical integration rather than an integration already shared from somewhere else

The source can be organization-owned or project-owned. Cross-organization sharing is still managed by owners of the
source organization; project membership alone does not authorize sending or revoking an invitation.

Only organization owners can send, accept, decline, or revoke an organization-sharing invitation. Only an owner of
the invited organization can delete the local shared integration because deletion also revokes the sharing
relationship.

## Send an invitation

As an owner of the source organization:

1. Open the OAuth integration.
2. Go to `Sharing`.
3. In `Share OAuth integration with another organization`, enter the target organization's exact machine name.
4. Click `Send invitation`.

Wodby always returns the same confirmation. It does not tell the sender whether that organization exists, whether it
is the source organization, whether it already has access, or whether an equivalent invitation is pending. If the
target is eligible, its owners receive an email with a review link. Repeated invitations to the same organization are
suppressed for at least 24 hours.

Pending invitations are deliberately not shown to the sender. The target organization appears on the source
integration's `Sharing` page only after one of its owners accepts.

## Review an invitation

As an owner of the invited organization:

1. Open `Integrations`.
2. Click `OAuth invitations`.
3. Review the source organization, provider account scope, and integration capabilities.
4. Choose the local integration name and title.
5. Accept the invitation, or decline it.

Invitations expire after seven days. Declining an invitation does not notify the source organization.

Acceptance creates an organization-owned integration in the invited organization. Use its normal `Sharing` page if
specific projects in that organization need access.

## Credential ownership and revocation

Wodby does not copy OAuth tokens, provider installation IDs, keys, or other credential material to the invited
organization. The new integration is a local handle, and Wodby validates the accepted relationship whenever it uses
the source credentials.

The source organization remains responsible for the provider connection. After an invitation is accepted, Wodby
freezes user-driven changes to the canonical integration while another organization depends on it. Its metadata,
capabilities, provider fields, ownership, in-organization sharing, and deletion cannot be changed until every active
organization share is revoked. Routine OAuth token refresh and provider maintenance continue so an ordinary token
renewal does not interrupt the invited organization.

The invited owner should accept only when they trust the source organization to maintain the provider connection and
coordinate any later change that requires revocation.

Source owners can see accepted organizations on the canonical integration's `Sharing` page and revoke access at any
time. Revocation takes effect immediately: the local integration is disabled and existing references can no longer
perform credential-backed operations. The invited organization keeps ownership of its references and can replace
them with another integration.

Deleting the invited organization's local integration also revokes the relationship, but it does not delete the
canonical integration or disconnect the provider account. A canonical integration cannot be changed or deleted while
it still has active organization shares; revoke them first.

## Privacy model

Organization lookup is intentionally one-way:

- the source receives no confirmation that a submitted organization name exists
- the source cannot view pending or declined invitations
- the invited organization's name becomes visible to the source only after acceptance
- only owners of the exact invited organization can open or act on the invitation link
- invitation details expose a limited integration summary, not source credentials or internal entity identifiers

The invited owners do see the source organization after Wodby has matched the invitation to their organization. This
lets them make an informed decision before accepting delegated credentials.

## Related pages

- [Integrations](index.md)
- [Sharing](../sharing.md)
- [Access control](../access-control.md)
