# Wodby Docs Review Checklist

Use this checklist when shipping a user-facing feature, pricing change, or dashboard workflow update.

## Product behavior

- Confirm the dashboard path used in the docs is still correct.
- Confirm any retention period, timeout, quota, or expiry value is still correct.
- Confirm plan or billing wording still matches `wodby.com` and the dashboard.
- Confirm feature status wording is still accurate, especially for `coming soon` items.

## Navigation and discoverability

- Add or update a public docs page if the feature introduces a new user workflow.
- Mention dashboard location inline only when it materially reduces ambiguity in a multi-step flow.
- Add or update a comparison guide if the feature changes how users choose between options.
- Add glossary terms if the feature introduces new nouns in the dashboard.

## Integrations and providers

- If a new provider manifest was added, create the matching docs page under `2.0/docs/integrations/`.
- Run `python3 2.0/scripts/validate_provider_docs.py`.
- Update provider catalog navigation in `2.0/mkdocs.yml` if needed.

## Apps, Kubernetes, and operations

- Update onboarding docs if the feature changes app creation or cluster creation.
- Update endpoint docs if domains, ports, auths, or ingress settings changed.
- Update app-service docs if a service submenu, operation, or limitation changed.
- Update backups docs if preset scope, scheduling, or storage behavior changed.

## Access and billing

- Update organization, project, sharing, or user-settings docs if permissions changed.
- Update pricing docs if plan capabilities or included credits changed.
- Update certificate docs if certificate handling or certificate UX changed.

## Verification

- Build the docs with `python3 -m mkdocs build -f 2.0/mkdocs.yml --strict`.
- Check that new pages are linked from navigation or a related page.
- Check that redirects are in place for renamed or removed pages when needed.
