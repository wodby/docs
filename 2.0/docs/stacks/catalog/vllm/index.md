# vLLM

The Wodby vLLM catalog stack runs one vLLM service that serves a Hugging Face model through an OpenAI-compatible API.
The current composition and defaults are in [`wodby/stack-vllm`](https://github.com/wodby/stack-vllm).

This stack is a preview release. End-to-end GPU inference and private-access validation are still required before
production use.

## Before you create the app

- **GPU capacity.** The cluster needs GPU nodes that vLLM can use. Each replica requests one GPU and runs only on Linux
  amd64 nodes. See [GPU node pools](../../../clusters/gpu.md) for the supported managed clusters.
- **Private access.** The stack requires [Private App Access](../../../apps/access.md) with the Private network type
  for the entire app. Select a compatible Private App Access integration when you create the app. This needs an active
  paid subscription and a cluster that uses managed app routing. vLLM's API key does not protect all of its management
  and metrics routes, so the stack does not publish a public route.

## Choose a model

Set these on the vLLM app service. Change the model and its revision together.

| Setting | Default | Notes |
| --- | --- | --- |
| **Hugging Face model** | `Qwen/Qwen3-0.6B` | A small model for a first test, not a production target |
| **Model revision** | A pinned commit | A commit, tag, or branch of the model |
| **API model name** | `model` | The name clients use, not the Hugging Face name |
| **Maximum context length** | `4096` | Input and output tokens per request. A higher value needs more VRAM |
| **GPUs used by each replica** | `1` | Also set the container's GPU count to this value. The GPUs must be on one node |
| **Fraction of GPU memory used by vLLM** | `0.9` | |
| **Hugging Face token** | Empty | Optional secret for private or gated models. Accept the model's license separately |

Check which model architectures vLLM supports before you pick another model. A model needs enough VRAM on the node.
Raise the app service's CPU and memory resources for a larger model.

## Call the API

Use the private address that Private App Access reports for the app, with `/v1` appended. Services in the same
environment can use `http://<app service name>:8000/v1`.

Open the vLLM app service's **Configuration > Tokens** tab and reveal `api_key`. Clients send it as a Bearer token.
Request `/v1/models` to list the served model name. See [Tokens](../../../apps/tokens.md).

The key protects the `/v1` routes. `/health` and `/metrics` answer without it, so keep the whole app private.
`/health` answers when the model is loaded.

## Replicas and updates

- The stack starts with one replica. Each replica needs its own GPUs. Three replicas at two GPUs each need six GPUs.
- An update stops a replica before it starts the replacement, so it needs no extra GPU. A single replica is unavailable
  during an update.
- Startup includes the model download and can take up to 29 minutes before Wodby treats the pod as failed.

## Model cache

By default, the model cache is per pod and limited to 20 GiB. It survives a container restart but is lost when the pod
is replaced, and every replica downloads its own copy.

The optional **Model cache** volume (50 GiB by default) keeps the cache across pod replacements, so the model is not
downloaded again. Its claim attaches to one node, so use it with a single replica. Add it from the app service's
volumes, or give it a size in the stack.

## Limits

- The stack does not provision machines, install GPU drivers, or buy external GPU capacity.
- Remote model code is not enabled.
- KServe, external GPU providers, Wodby Cloud GPU billing, and token-aware scaling are not part of this stack.
- AMD, CPU-only inference, MIG configuration, multi-node tensor parallelism, and GPU sharing are not part of this stack.

For client examples, see [`wodby/llm-inference-boilerplate`](https://github.com/wodby/llm-inference-boilerplate).
