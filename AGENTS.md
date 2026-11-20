# Wodby documentation

`2.0/` is the Wodby 2 documentation and `1.0/` is the Wodby 1 documentation. They are separate sites with separate
builds; a change to one does not apply to the other.

## What belongs in the docs

The docs are for customers who use Wodby to deploy, configure, operate and troubleshoot their applications. Keep a
passage only if it passes both tests:

1. **It helps the customer.** After reading it, they can do something, decide something or fix something they could
   not before.
2. **It describes the product, not its implementation.** Leave out how Wodby works inside, even when a customer might
   find it interesting or useful. State the requirement or the outcome, not the mechanism. For example, write "TCP
   ports 80 and 443 on the server's public IP must reach the server", not how Wodby checks them.

Keep:

- supported interfaces: dashboard steps, CLI commands, the REST and MCP references, manifest fields, settings
  customers choose and environment variables Wodby sets in their apps
- prerequisites and requirements, such as ports, firewall and proxy allowlists, hardware, operating systems,
  permissions and cloud IAM policies
- limits, failure behavior and how to recover, downtime and data-loss warnings, and troubleshooting steps customers
  can perform, with the messages they will see

Leave out:

- how a feature works inside: checks and how they run, algorithms, retries, polling intervals and internal timeouts,
  caching, ordering of internal steps, and where data is stored
- names customers never type, set or see in the dashboard: internal components, tasks, steps, jobs, database tables,
  configuration keys, and the Kubernetes objects, Helm releases, labels and namespaces Wodby creates, unless a
  documented customer action needs them
- internal hostnames and ports, unless customers must allow, reach or configure them
- architecture, design rationale, the history of how behavior changed, rollout notes and internal version numbers
- how the product is tested ("supported", not "tested with"), and version numbers the dashboard already shows
- for security features, the mechanism behind a guarantee: state the guarantee only
- steps the dashboard already prompts for at the moment they are needed, unless the page adds something the dashboard
  cannot show

When a passage mixes an outcome with its mechanism, keep the outcome and drop the mechanism.

## Page titles and descriptions

These rules apply to both sites.

- The first heading of a page is its browser and search title. Write it so it makes sense on its own: "Cluster
  updates", not "Updates". Use sentence case.
- Wodby 2: head a catalog stack guide "<Product> stack guide", or "<Product> (buildable) stack guide", and a provider
  page "<Product> provider".
- Wodby 1: head a stack page "<Product> stack guide" and an integration page "<Product> integration".
- Keep the navigation label in `mkdocs.yml` short. It does not affect the title.
- Add a `title` to the front matter only when the title should say more than the heading.
- Give every page a `description` in its front matter: one or two plain sentences, 110 to 160 characters, no Markdown.
  Update it when the page's subject changes, for example when a list in it gains a new item.

The title and description build hooks and their tests are shared in `scripts/`. The details are in
[`2.0/scripts/README.md`](2.0/scripts/README.md).

## Before pushing

```sh
python3 -m unittest discover -s scripts
python3 -m unittest discover -s 2.0/scripts -p 'test_*.py'
(cd 1.0 && sh scripts/check-docs.sh -d ../sites/1.0)
(cd 2.0 && mkdocs build --strict -d ../sites/2.0)
```

The tests fail when two pages share a title, a page is titled with a menu label such as "Overview", a stack or provider
page (or a Wodby 1 stack or integration page) does not say what it is, or a description is missing or outside the length
limits.
