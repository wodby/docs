---
description: Deploy Open WebUI, a self-hosted chat interface for AI models, on Wodby with the Open WebUI catalog stack and PostgreSQL, and connect it to model APIs.
---

# Open WebUI

The Wodby Open WebUI catalog stack runs [Open WebUI](https://openwebui.com/), a self-hosted chat interface for AI
models, with PostgreSQL. The current composition is documented in
[`wodby/stack-open-webui`](https://github.com/wodby/stack-open-webui).

Open WebUI does not run models itself. It connects to model APIs: a hosted provider such as OpenAI, or your own
OpenAI-compatible server.

## Administrator account

Set the administrator in the Open WebUI service's settings when you create the app. Both settings are required:

| Setting | What it sets |
| --- | --- |
| Admin email | The email address the administrator signs in with |
| Admin password | The administrator's password |

Open WebUI creates this account on its first start and then turns public sign-up off, so nobody else can register.
Open the app's domain and sign in with these credentials.

The settings are only used when the database has no users. To change the password later, use Open WebUI. To let other
people in, add their accounts in **Admin Panel → Users**, or turn sign-up back on in
**Admin Panel → Settings → General**.

## Connect models

Add a model connection in **Admin Panel → Settings → Connections**: an API key for a hosted provider, or the URL and
key of an OpenAI-compatible server, for example `https://your-server/v1`. The models it offers then appear in the chat.

In a [custom stack](../../create.md), the Open WebUI service's optional **OpenAI-compatible API** link can connect it to
a service in the same app that offers such an API, such as [vLLM](../vllm/index.md), including the service's API key.
The link only takes effect on Open WebUI's first start; see the next section.

## Settings saved by Open WebUI

On its first start, Open WebUI saves most of its configuration in the database, including model connections, sign-up,
and its own address. After that, it ignores the environment variables for those settings, and changes made in
**Admin Panel → Settings** survive deployments. As a result, a model link added to an existing app does not add a
connection; add it in Open WebUI instead.

Setting the environment variable `RESET_CONFIG_ON_START` to `true` makes Open WebUI read the variables again on the next
start, but it also discards every setting changed in the admin panel. See
[Environment variables](../../../apps/environment-variables.md).

## Domains

Only the app's own domains can open the chat's live connection or call Open WebUI's API from a browser. When you add or
remove a domain, Wodby marks the Open WebUI service for redeployment; deploy it to apply the change. To allow other
origins, set the `CORS_ALLOW_ORIGIN` environment variable on the service to a list of origins separated by `;`, such as
`https://chat.example.com;https://intranet.example.com`. It replaces the computed list.

Answers stream for as long as the model writes, so the route has no request timeout. Do not set the route's request
body size: it makes the route hold each request in memory until it is complete, and the chat's live connection stops
working. See [HTTP settings](../../../apps/endpoints.md#http-settings).

## Data and backups

- PostgreSQL holds users, chats, settings, models, and prompts.
- The Open WebUI volume (10 GB by default) holds uploaded files, the document search index, and caches.

Back up the database and the Open WebUI volume together as one recovery set. The Open WebUI service has no backup or
import operation in Wodby. The PostgreSQL service does. See [Backups](../../../apps/backups.md).

Document search runs its embedding model inside the Open WebUI container, using the models that come with the image.
Large documents need memory and CPU in that container.

## Limits

- The Open WebUI service is fixed to one replica. Several replicas would need pgvector, Redis, and storage shared
  between replicas, which this stack does not set up.
- There is no Ollama service in the catalog, so Open WebUI's Ollama connection is turned off.
- Open WebUI's [license](https://docs.openwebui.com/license) requires keeping its branding in larger deployments.
  Wodby runs the official image unchanged.
