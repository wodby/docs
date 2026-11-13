---
description: Deploy Discourse with plugins that don't ship with it on Wodby with the buildable Discourse stack, which adds the plugins listed or committed in your Git repository.
---

# Discourse (buildable)

The buildable Discourse stack runs [Discourse](https://www.discourse.org/) with plugins that don't ship with it: your
Git repository lists them or holds them, and Wodby builds Discourse with them. The stack has the same services as the
[Discourse stack](../discourse/index.md): PostgreSQL, Redis and OpenSMTPD. Its composition is documented in
[`wodby/stack-discourse-buildable`](https://github.com/wodby/stack-discourse-buildable).

Everything in the [Discourse guide](../discourse/index.md) applies, from the administrator emails to mail, data and
upgrades. This page covers what differs.

## Repository

Start the repository from the [Discourse boilerplate](https://github.com/wodby/discourse-boilerplate) and connect it
when you create the app.

| Path | Purpose |
| --- | --- |
| `plugins.txt` | Plugins to clone, one Git repository URL per line, optionally followed by a branch or tag |
| `plugins/` | Plugins committed to the repository, one directory per plugin with its `plugin.rb` |

For example:

```
https://github.com/discourse/discourse-bbcode.git
https://github.com/example/discourse-my-plugin.git v1.2.0
```

## Build

Choose the Discourse release line when you create the app. The build starts from Wodby's Discourse image of that line,
adds your plugins, installs their gems and compiles only their JavaScript: Discourse's own is reused from the image.

The build fails when a plugin has the name of a plugin that ships with Discourse, such as chat, solved or data
explorer, when a directory has no `plugin.rb`, or when a repository can't be cloned. Turn the plugins that ship with
Discourse on in its settings instead.

A plugin must support the release line you run. Pin a plugin to a branch or tag that does, for example the branch a
plugin keeps for the extended support release.

## Plugins and updates

Discourse migrates its database when it starts, plugins' migrations included. A plugin removed from the repository
disappears from Discourse on the next deployment; its data stays in the database.

Discourse's version comes from the service version and its image, not from the repository. It moves forward with
service updates, and the app's next build uses it.

To run Discourse with only the plugins it ships with, use the [Discourse stack](../discourse/index.md).
