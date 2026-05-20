# Single Sign-On

Single Sign-On (SSO) lets users sign in to Wodby through your organization's identity provider.

SSO is configured at the organization level from `Organization > SSO`. It is currently an additional sign-in option and does not disable email/password sign-in, GitHub sign-in, Google sign-in, or API keys.

## Supported protocol

Wodby currently supports OpenID Connect (OIDC).

Common OIDC identity providers include:

- Okta
- Microsoft Entra ID
- Google Workspace
- Auth0
- ZITADEL
- Keycloak

The dashboard currently manages one OIDC provider per organization. SAML, SCIM directory sync, role mapping, and mandatory SSO enforcement are not supported yet.

## Who can configure SSO

Organization owners and admins can manage SSO providers.

Users who sign in through SSO must have an email address that matches one of the verified SSO domains configured for the organization.

## How SSO access works

When SSO is enabled for an organization:

- users can choose `Single Sign-On` on the sign-in page
- users enter the organization name and are redirected to the configured identity provider
- Wodby accepts only verified email addresses returned by the identity provider
- new users can be created automatically when Just-in-Time provisioning is enabled
- Just-in-Time users are added to the organization with the `Member` role

SSO does not change existing organization roles for current members.

## Before you start

Prepare the following values from your identity provider:

- OIDC issuer URL
- OIDC client ID
- OIDC client secret
- one or more email domains allowed to use this SSO provider

In your identity provider, create an OIDC web application and add the Wodby SSO callback URL as an allowed redirect URI:

```text
https://<wodby-dashboard-domain>/auth/sso/callback
```

Use the dashboard domain you normally use to sign in to Wodby.

The OIDC application must be allowed to request these scopes:

```text
openid profile email
```

The identity provider must return a stable subject identifier and a verified email claim.

## Configure OIDC SSO

Open `Organization > SSO`.

1. Click `Enable SSO`.
2. Enter a provider name, such as `Okta` or `Microsoft Entra ID`.
3. Enter the OIDC issuer URL.
4. Enter the OIDC client ID.
5. Enter the OIDC client secret.
6. Add the email domains that should be allowed to sign in through this provider.
7. Choose whether Just-in-Time provisioning should be enabled.
8. Click `Create OIDC provider`.

New providers are created disabled. Wodby shows domain verification records after the provider is created.

## Verify SSO domains

Each SSO domain must be verified before the provider can be enabled.

After saving the provider, Wodby shows a DNS `TXT` record for each domain. Add the exact record name, type, and value in your DNS provider.

The record looks like this:

```text
_wodby-sso.example.com TXT "wodby-sso-verification=<token>"
```

After the DNS record is published, click `Verify domain`.

DNS propagation can take time. If verification fails, wait a few minutes and try again.

## Enable SSO

After every configured domain is verified, enable the provider from `Organization > SSO`.

Wodby blocks enabling an SSO provider while any configured domain is unverified. If you edit the domain list later, newly added domains must be verified before SSO can be enabled again.

## Update SSO settings

You can update the provider name, issuer URL, client ID, client secret, allowed domains, and Just-in-Time provisioning setting from `Organization > SSO`.

The OIDC client secret is write-only. Leave the client secret field blank when you want to keep the existing secret.

If SSO is enabled and you add or change domains, Wodby disables SSO until every configured domain is verified again.

## Sign in with SSO

To sign in:

1. Open the Wodby sign-in page.
2. Choose `Single Sign-On`.
3. Enter the organization name.
4. Continue to the identity provider.
5. Complete authentication with your identity provider.

If the organization has one enabled SSO provider, Wodby redirects directly to that provider. If more than one provider is available, choose the provider first.

## Invitations and Just-in-Time provisioning

If an invited user signs in with SSO, the email returned by the identity provider must match the invitation email.

If Just-in-Time provisioning is enabled, a user whose verified email domain matches the SSO provider can be created automatically and added as an organization `Member`.

If Just-in-Time provisioning is disabled, the user must be invited before signing in with SSO.

## Disabling SSO

Disabling an SSO provider stops new SSO sign-ins through that provider.

Disabling SSO does not:

- delete Wodby users
- remove organization memberships
- revoke API keys
- disable email/password sign-in
- disable GitHub or Google sign-in

## Security notes

- Verify only domains your organization controls.
- Do not share the OIDC client secret.
- Use a dedicated OIDC application for Wodby.
- Keep at least one owner account able to sign in without SSO until mandatory SSO enforcement is available.
- Review organization membership regularly when Just-in-Time provisioning is enabled.

## Related pages

- [Organization](org.md)
- [Access control](access-control.md)
- [User identities](user/identities.md)
- [API keys](user/api-keys.md)
