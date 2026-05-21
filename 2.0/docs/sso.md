# Single Sign-On

Single Sign-On (SSO) lets users sign in to Wodby through your organization's identity provider.

SSO is configured at the organization level from `Organization > SSO`. It is currently an additional sign-in option and does not disable email/password sign-in, GitHub sign-in, Google sign-in, or API keys.

## Supported providers

Wodby supports multiple SSO providers per organization.

Supported provider kinds:

- **OIDC** for OpenID Connect providers such as Okta, Microsoft Entra ID, Auth0, ZITADEL, or Keycloak
- **Google Workspace** for Google-managed organization domains
- **GitHub Organization** for GitHub organization membership checks
- **SAML 2.0** for SAML identity providers

SCIM directory sync, role mapping, and mandatory SSO enforcement are not supported yet.

## Who can configure SSO

Organization owners and admins can manage SSO providers.

Users who sign in through SSO must match the access rules of the selected provider. Most providers require a verified email address on a verified domain configured in Wodby.

## How SSO access works

When SSO is enabled for an organization:

- users can choose `Single Sign-On` on the sign-in page
- users enter the organization name and are redirected to an enabled SSO provider
- if more than one provider is available, users choose the provider before continuing
- Wodby checks the identity returned by the provider against the provider rules
- new users can be created automatically when Just-in-Time provisioning is enabled
- Just-in-Time users are added to the organization with the `Member` role

SSO does not change existing organization roles for current members.

## Domain verification

OIDC, Google Workspace, and SAML 2.0 providers require at least one email domain. Each domain must be verified before the provider can be enabled or used for sign-in.

GitHub Organization providers can be configured without domains. If domains are added to a GitHub Organization provider, Wodby also enforces email-domain matching and those domains must be verified.

After saving a provider with domains, Wodby shows a DNS `TXT` record for each domain. Add the exact record name, type, and value in your DNS provider.

The record looks like this:

```text
_wodby-sso.example.com TXT "wodby-sso-verification=<token>"
```

After the DNS record is published, click `Verify domain`.

DNS propagation can take time. If verification fails, wait a few minutes and try again.

When the last required domain for a provider is verified, Wodby enables that provider automatically. Providers that do not require domain verification, such as a GitHub Organization provider without domains, can be enabled immediately when they are created.

## Configure an OIDC provider

Prepare the following values from your identity provider:

- OIDC issuer URL
- OIDC client ID
- OIDC client secret
- one or more email domains allowed to use this provider

In your identity provider, create an OIDC web application and add the Wodby SSO callback URL as an allowed redirect URI:

```text
https://apps.wodby.com/auth/sso/callback
```

Use the dashboard domain you normally use to sign in to Wodby.

The OIDC application must be allowed to request these scopes:

```text
openid profile email
```

The identity provider must return a stable subject identifier and a verified email claim.

To create the provider:

1. Open `Organization > SSO`.
2. Click `New provider`.
3. Choose `OIDC`.
4. Enter a provider name, issuer URL, client ID, and client secret.
5. Add the email domains allowed to sign in through this provider.
6. Choose whether Just-in-Time provisioning should be enabled.
7. Click `Create provider`.
8. Verify every configured domain.
9. After the last domain is verified, Wodby enables the provider automatically.

The OIDC client secret is write-only. When editing an OIDC provider, leave the client secret field blank to keep the existing secret.

## Configure a Google Workspace provider

Google Workspace providers use Wodby's Google OAuth application. You do not need to create your own Google OAuth client.

Prepare one or more Google Workspace email domains, such as `example.com`.

To create the provider:

1. Open `Organization > SSO`.
2. Click `New provider`.
3. Choose `Google Workspace`.
4. Enter a provider name.
5. Add the Google Workspace email domains allowed to sign in through this provider.
6. Choose whether Just-in-Time provisioning should be enabled.
7. Click `Create provider`.
8. Verify every configured domain.
9. After the last domain is verified, Wodby enables the provider automatically.

During sign-in, Wodby requires a Google verified email address and a hosted domain claim that matches one of the provider domains.

## Configure a GitHub Organization provider

GitHub Organization providers use Wodby's GitHub OAuth application and require membership in a GitHub organization.

Prepare the GitHub organization slug or URL, such as `wodby` or `https://github.com/wodby`.

Domains are optional. If you add domains, Wodby also checks the user's verified primary GitHub email domain.

To create the provider:

1. Open `Organization > SSO`.
2. Click `New provider`.
3. Choose `GitHub Organization`.
4. Enter a provider name.
5. Enter the GitHub organization slug or URL.
6. Optionally add email domains allowed to sign in through this provider.
7. Choose whether Just-in-Time provisioning should be enabled.
8. Click `Create provider`.
9. Verify any configured domains.

If no domains are configured, Wodby enables the provider immediately after it is created. If domains are configured, Wodby enables the provider after the last domain is verified.

During sign-in, Wodby requires GitHub organization membership and a verified primary GitHub email. If the provider has no domains, users must select the provider from the organization's SSO provider list because email-domain discovery cannot identify it.

## Configure a SAML 2.0 provider

Prepare one of the following from your identity provider:

- IdP metadata URL
- IdP metadata XML

Also prepare one or more email domains allowed to use this provider.

To create the provider:

1. Open `Organization > SSO`.
2. Click `New provider`.
3. Choose `SAML 2.0`.
4. Enter a provider name.
5. Enter either the IdP metadata URL or the IdP metadata XML.
6. Add the email domains allowed to sign in through this provider.
7. Choose whether Just-in-Time provisioning should be enabled.
8. Click `Create provider`.
9. Configure Wodby as a service provider in your identity provider.
10. Verify every configured domain.
11. After the last domain is verified, Wodby enables the provider automatically.

After the provider is created, Wodby shows SAML setup values:

- IdP entity ID parsed from the metadata
- Wodby service provider entity ID
- Wodby service provider metadata URL
- Assertion Consumer Service (ACS) URL

Use the service provider metadata URL when your identity provider can import SP metadata. Otherwise, configure the service provider entity ID and ACS URL manually.

The service provider metadata URL is public and returns Wodby's SAML SP metadata XML for that provider.

When editing a SAML 2.0 provider, leave both metadata fields blank to keep the existing IdP metadata. Enter a metadata URL or metadata XML only when replacing the IdP metadata. Do not enter both at the same time.

The SAML assertion must include a stable subject identifier and an email address that matches a verified provider domain.

## Provider enablement

Providers that require domain verification are created disabled.

After every required domain is verified, Wodby enables the provider automatically.

Wodby does not enable an SSO provider while any configured domain is unverified. If you edit the domain list later, Wodby disables the provider until every configured domain is verified again.

## Update SSO settings

You can update the provider name, provider-specific settings, allowed domains, and Just-in-Time provisioning setting from `Organization > SSO`.

If a provider is enabled and you add or change domains, Wodby disables that provider and enables it again after every configured domain is verified.

Provider kind cannot be changed after creation. Create a new provider when you need a different protocol or identity source.

## Sign in with SSO

To sign in:

1. Open the Wodby sign-in page.
2. Choose `Single Sign-On`.
3. Enter the organization name.
4. If prompted, choose the SSO provider.
5. Complete authentication with the identity provider.

If the organization has one enabled SSO provider, Wodby redirects directly to that provider. If more than one provider is available, choose the provider first.

## Invitations and Just-in-Time provisioning

If an invited user signs in with SSO, the email returned by the identity provider must match the invitation email.

If Just-in-Time provisioning is enabled, a user whose identity matches the SSO provider rules can be created automatically and added as an organization `Member`.

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
- Use dedicated identity-provider applications for Wodby.
- Do not share OIDC client secrets or SAML metadata XML from private IdPs.
- For SAML providers, prefer metadata URLs when your IdP rotates signing certificates.
- Keep at least one owner account able to sign in without SSO until mandatory SSO enforcement is available.
- Review organization membership regularly when Just-in-Time provisioning is enabled.

## Related pages

- [Organization](org.md)
- [Access control](access-control.md)
- [User identities](user/identities.md)
- [API keys](user/api-keys.md)
