# Wodby 2.0 Docs Backlog

Internal backlog for improving public docs under `2.0/docs/` based on current behavior in:

- `~/Projects/backend`
- `~/Projects/dashboard`
- `wodby.com`

This file is not meant for public navigation. It is a working backlog for docs updates.

## Locked decisions

- Mention Wodby Cloud explicitly in onboarding and cluster docs.
- Treat Demo as a demo mode on Wodby Cloud, not as a separate platform concept.
- Demo retention is 24 hours.
- State that custom certificate upload is coming soon.
- Create docs pages for every provider, including variable-only providers.
- For variable-only providers, lightweight pages are acceptable. Listing setup fields and resulting env vars is enough.
- Treat `Providers` and `Integrations` as separate docs concepts, same as in the dashboard.
- Make `Providers` a top-level docs section in navigation, with `Integrations` focused on creating and using connections.
- Do not add generic `Path in dashboard` callout blocks. Mention dashboard locations inline only when they actually reduce ambiguity.
- Current certificate wording should say custom certificate upload is coming soon.
- Future direction for certificate UX: users should be able to select existing org certificates for endpoints once custom cert support ships.

## Target information architecture

Recommended target shape for public docs navigation:

- Getting Started
- Apps
- Kubernetes
- Databases
- CI/CD
- Providers
- Integrations
- Access & Billing
- Reference
- Development

Notes:

- `Providers` should answer: what third-party services exist, what fields are required, and what variables or capabilities they expose.
- `Integrations` should answer: how to create connections and where those connections are used.
- Service templates, stack templates, schema-like pages, and low-level manifest mechanics should gradually move under `Reference`.

## Priority legend

- `P0` accuracy or trust issue
- `P1` missing high-value product documentation
- `P2` structure, discoverability, and UX improvement
- `P3` maintenance and automation

## P0

- [x] Update onboarding to reflect the real deployment entry points
  Goal: `Getting started` should describe the current platform, not an older managed-Kubernetes-only flow.
  Files:
  - `2.0/docs/index.md`
  - `2.0/docs/kubernetes/index.md`
  Notes:
  - Mention three cluster paths clearly: managed Kubernetes, K3S, Wodby Cloud.
  - Explain that Demo is a Wodby Cloud demo cluster.
  - Replace outdated wording like "Wodby does not currently provide Kubernetes cluster out of the box".
  - Fix copy issues such as `Azure AKZ`, `under you account`, and general grammar.

- [x] Rewrite app creation Step 2 to match the current wizard
  Goal: the docs must match the actual `Destination` step in the dashboard.
  Files:
  - `2.0/docs/apps/index.md`
  Notes:
  - Document `My clusters` vs `Wodby Cloud`.
  - Document Wodby Cloud persistent clusters, paid-plan requirement, regions, machine types, and node count inputs.
  - Document Demo as the Wodby Cloud demo option.
  - Make clear that K3S is created from `Kubernetes > Connect server`, not from the app form.

- [x] Fix demo cluster lifetime mismatch
  Goal: all docs should use the same demo retention period as the product.
  Files:
  - `2.0/docs/kubernetes/demo.md`
  - `2.0/docs/kubernetes/index.md`
  - `2.0/docs/index.md`
  Notes:
  - Current docs say 12 hours.
  - Current dashboard copy says 24 hours.
  - Confirm product truth once before publishing, then update all docs consistently.

- [x] Resolve the certificate support contradiction
  Goal: users should not get conflicting messages about custom certificate upload.
  Files:
  - `2.0/docs/org.md`
  - `2.0/docs/apps/endpoints.md`
  - new page: `2.0/docs/certs.md` or `2.0/docs/org/certs.md`
  Notes:
  - Public wording should say custom certificate upload is coming soon.
  - Explain what exists today: automatic Let's Encrypt handling and org-level certificate visibility.
  - Do not claim upload support until the UI is enabled.

- [x] Align pricing docs with current plan messaging
  Goal: the docs should reflect the same plan story as the pricing page and dashboard.
  Files:
  - `2.0/docs/pricing.md`
  Notes:
  - Mention Team-plan capabilities already surfaced publicly: custom domains, auto backups, cron jobs, web shell, 1000 compute credits monthly.
  - Keep prices delegated to `wodby.com/pricing`, but make plan differences concrete.
  - Clarify Wodby Cloud costs vs app-service billing vs cloud-provider costs.

- [x] Expand the provider and integrations catalog to cover the actual provider set
  Goal: docs should not look smaller than the real product.
  Files:
  - `2.0/docs/integrations/index.md`
  - `2.0/docs/integrations/providers.md`
  - `2.0/docs/integrations/types.md`
  - new provider pages under `2.0/docs/integrations/`
  Notes:
  - Existing docs cover only part of the provider manifest set.
  - Create a page for every provider manifest.
  - Start with lightweight pages for variable-only providers:
    `algolia`, `anthropic`, `auth0`, `cloudflare`, `discord`, `gemini`, `intercom`, `mailchimp`, `openai`, `pusher`, `slack`, `stripe`, `tailscale`, `telegram`, `twilio`.
  - For lightweight pages, include:
    - what the provider is used for
    - required fields
    - env vars exposed
    - integration kind or provider type
  - Remove or update "coming soon" pages when the provider exists in product behavior.

## P1

- [x] Add a Wodby Cloud guide that matches the real product flow
  Goal: explain when to use Wodby Cloud, how it differs from managed Kubernetes and K3S, and how billing works.
  Files:
  - `2.0/docs/kubernetes/wodby-cloud.md`
  Notes:
  - Add a small comparison table: managed Kubernetes vs K3S vs Wodby Cloud vs Wodby Cloud demo.
  - Explain that persistent Wodby Cloud clusters require a paid plan.
  - Explain compute credits in user language, not just billing terms.

- [x] Expand the K3S guide into a real walkthrough
  Goal: document the full `Connect server` workflow rather than a short summary.
  Files:
  - `2.0/docs/kubernetes/k3s.md`
  Notes:
  - Show the dashboard path.
  - Explain that Wodby generates a time-limited install command.
  - Mention optional monitoring toggle at creation time.
  - Add troubleshooting notes for `Awaiting` state and command expiration.

- [x] Document project access and resource boundaries
  Goal: explain how projects actually work in day-to-day usage.
  Files:
  - `2.0/docs/projects.md`
  - `2.0/docs/teams.md`
  - new page: `2.0/docs/access-control.md`
  Notes:
  - Explain project `Resources`, `Access`, and sharing model.
  - Explain direct memberships vs team-based access and project roles: read, write, admin.
  - Explain that cross-project resource references are not allowed.

- [x] Add docs for sharing resources across projects
  Goal: users should understand sharing without exploring each entity screen manually.
  Files:
  - new page: `2.0/docs/sharing.md`
  Notes:
  - Cover sharing behavior for apps, clusters, databases, integrations, stacks, services, and providers.
  - Explain practical implications and limitations.

- [x] Add user settings and security docs
  Goal: document the whole user settings area, not only API keys.
  Files:
  - new section under `2.0/docs/user/` or equivalent
  Suggested pages:
  - `account.md`
  - `security.md`
  - `api-keys.md`
  - `ssh-keys.md`
  - `emails.md`
  - `identities.md`
  Notes:
  - Security page should cover password changes, 2FA enrollment, 2FA disable, and recovery codes.
  - SSH keys page should mention that keys are propagated to SSHD app services you can write to and may trigger redeploys.
  - Emails page should cover primary vs secondary emails and verification.
  - Identities page should cover linked OAuth identities.

- [x] Add an org settings guide
  Goal: make org-level operations discoverable in one place.
  Files:
  - `2.0/docs/org.md`
  - new pages if needed for `backups`, `certs`, `billing`, `envs`
  Notes:
  - Split `Organization` into overview plus settings subtopics.
  - Cover members, teams, environments, backup presets, billing, certificates, and defaults for CI and registry.

- [x] Add backup preset docs
  Goal: explain org-wide vs app-level vs database-level presets clearly.
  Files:
  - `2.0/docs/apps/backups.md`
  - `2.0/docs/databases/backups.md`
  - new page: `2.0/docs/backups.md`
  Notes:
  - Explain how presets are reused.
  - Explain org-wide backup presets as a separate concept.
  - Mention destination bucket and storage-class behavior.

- [x] Expand endpoint docs with auths and settings
  Goal: bring the docs in line with the actual endpoint submenu.
  Files:
  - `2.0/docs/apps/endpoints.md`
  Notes:
  - Document domains, ports, settings, and auths as first-class endpoint features.
  - Explain endpoint settings as ingress annotations in user language.
  - Explain basic auth scope options: app-level, service-level, domain-level.

- [x] Add app-service operations guide
  Goal: explain what users can do inside `Apps > [Instance] > Services > [Service]`.
  Files:
  - `2.0/docs/apps/services.md`
  - new page: `2.0/docs/apps/app-service-overview.md` if needed
  Notes:
  - Add `Overview`, `Configure`, `Database`, `Integrations`, `Env vars`, `Helm`, `Resources`, `Links`, `Volumes`, `Settings`, `Configs`, `Tokens`, `Annotations`.
  - Document the web terminal.
  - Explain when fields are unavailable for external or derivative services.

- [x] Add project resource overview docs
  Goal: show how resources are grouped and filtered in project context.
  Files:
  - `2.0/docs/projects.md`
  Notes:
  - Explain project-scoped filtering in the header.
  - Explain that Apps, Kubernetes, Databases, Integrations, Stacks, Services, Providers, and Tasks are viewed through selected projects.

- [x] Add overview pages for each integration type
  Goal: make each integration type understandable on its own before users dive into provider-specific setup.
  Files:
  - `2.0/docs/integrations/index.md`
  - new pages under `2.0/docs/providers/`
  Notes:
  - Add one overview page per type: Kubernetes, Databases, Storage, Git, CI, Registry, SMTP, VPN, and Variable.
  - Place those overview pages in the `Providers` section so each provider group starts with an explanation.
  - Link from each overview page to the matching provider docs.
  - Keep provider-specific credential fields on provider pages; keep type-level concepts on the group overview pages.

- [x] Expand the Development section into real developer documentation
  Goal: replace thin API and CLI stubs with task-oriented docs that are usable without reading source code.
  Files:
  - `2.0/docs/dev/api.md`
  - `2.0/docs/dev/cli.md`
  - `2.0/docs/dev/api-keys.md`
  - new pages if needed under `2.0/docs/dev/`
  Notes:
  - Explain API authentication, organization scoping, and how API keys relate to GraphQL, REST, and CLI usage.
  - Document the practical split between GraphQL and REST instead of only naming both.
  - Add example requests, common workflows, and error-handling guidance.
  - Expand CLI docs with installation, authentication, common commands, and CI-oriented examples.

## P2

- [ ] Optional targeted navigation refinement
  Goal: revisit navigation only if we want specific, narrow discoverability improvements without changing the core top-level product sections.
  Files:
  - `2.0/mkdocs.yml`
  Notes:
  - Keep core top-level entity sections such as `Stacks` and `Services`.
  - Do not introduce a generic `Reference` top-level section without an explicit product-docs decision.
  - Prefer small, targeted nav changes over broad restructures.
  - Add navigation entries for User settings, Sharing, Access control, Providers, and Certificates.
  - Keep `Providers` top-level instead of burying it under `Integrations`, because the dashboard exposes both separately.

- [x] Add comparison pages and decision guides
  Goal: reduce ambiguity in platform choices.
  Suggested pages:
  - managed Kubernetes vs K3S vs Wodby Cloud
  - app backups vs database backups
  - provider vs integration vs variable provider
  - app vs app instance vs app service

- [x] Add glossary and terminology cleanup
  Goal: use the same nouns as the dashboard and backend everywhere.
  Files:
  - new page: `2.0/docs/glossary.md`
  - touch core overview pages
  Notes:
  - Normalize `Wodby Cloud`, `Demo`, `Provider`, `Integration`, `Stack`, `Service`, `App instance`, `App service`, `Environment`.

- [x] Improve overview pages visually
  Goal: make landing pages easier to scan before diving into reference details.
  Notes:
  - Add comparison tables.
  - Add concise intro guidance instead of generic "When to use this section" blocks.
  - Add "Related pages" blocks.
  - Add more diagrams where they explain relationships well.

- [ ] Add screenshots where UI behavior matters (Deferred)
  Goal: reduce ambiguity in multi-step flows.
  Notes:
  - Deferred for now because dashboard screenshots need manual preparation before publication.
  Suggested targets:
  - app creation Step 2
  - K3S connect server
  - project access
  - org backup presets
  - endpoint auths
  - billing subscription page

- [x] Tighten copy across core pages
  Goal: improve clarity and polish.
  Scope:
  - grammar
  - singular/plural
  - consistent capitalization
  - remove stale "currently" phrasing unless it is maintained
  - replace implementation-heavy wording with user-facing language where possible

## P3

- [x] Generate or validate provider docs against backend manifests
  Goal: prevent the provider catalog from drifting again.
  Inputs:
  - `~/Projects/backend/pkg/provider/manifests/*.yml`
  Notes:
  - At minimum, add a check that every provider manifest has a matching docs page or is intentionally excluded.

- [x] Add a docs review checklist for feature launches
  Goal: make docs updates part of shipping.
  Suggested checklist items:
  - user-facing dashboard path changed
  - pricing/plan behavior changed
  - limits or retention period changed
  - new provider/integration added
  - new app-instance or cluster operation added

- [ ] Optional docs data source for lightweight provider pages
  Goal: reduce copy-paste work for variable-only providers.
  Notes:
  - A lightweight generator could build provider pages from manifest fields, instructions, and env var names.

## Suggested delivery order

### Batch 1

- onboarding and app creation flow
- demo wording
- Wodby Cloud page
- certificate wording fix
- pricing alignment

### Batch 2

- providers catalog expansion
- project access and sharing docs
- endpoint auths and settings docs
- app-service operations and web terminal docs

### Batch 3

- user settings and security docs
- org settings breakdown
- backup preset docs
- navigation restructure

### Batch 4

- screenshots
- glossary
- automation and validation

## Certificate direction

- Keep today’s docs conservative and say custom certificate upload is coming soon.
- When the feature ships, plan docs around this model:
  - upload or manage certificates at org level
  - select an existing certificate from endpoint configuration
