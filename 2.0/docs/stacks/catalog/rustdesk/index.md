---
description: Run the open-source RustDesk server on Wodby with the RustDesk Server catalog stack, so your devices use your own server for remote desktop sessions.
---

# RustDesk Server

The Wodby RustDesk Server catalog stack runs the open-source [RustDesk](https://rustdesk.com/) server, so your devices
use your own server for remote desktop sessions instead of RustDesk's public one. The current composition is documented
in [`wodby/stack-rustdesk`](https://github.com/wodby/stack-rustdesk).

The server has no web interface: you use it from the RustDesk app on each device. Devices connect over WebSocket to the
app's HTTPS domain, so it works on any cluster and you don't need to publish ports. The domain also shows a page with
these setup steps.

## Set up devices

1. Create an app from the **RustDesk Server** catalog stack and deploy it.
2. On the RustDesk app service, run the **Show client settings** action. See [Actions](../../../apps/services.md#actions).
   The task log shows the values to enter.
3. In the RustDesk app on each device, open **Settings > Network**:
    1. Turn on **Use WebSocket**.
    2. Under **ID/Relay server**, enter the **ID server**, **API server** and **Key** from the task log, and leave
       **Relay server** empty.

The ID server is the app's main domain, for example `prod.myapp.example.com`, and the API server is the same domain
with `https://`. The RustDesk app needs the API server to connect securely; the server has no accounts or address book.

The key is the server's public key: devices without it can't use the server, so share it only with people who should
use your server. The page on the app's domain shows the other values, but not the key.

## Connect devices without WebSocket

On [K3s](../../../clusters/k3s.md) clusters and
[single-node clusters](../../../clusters/managed.md#single-node-clusters), devices can also connect without
**Use WebSocket**:

1. Open **Apps > [App] > [Environment] > Endpoints > Ports**, select the `rustdesk` endpoint, and publish the `id` TCP
   port, then the `id-udp` UDP port. The second one gets the same public port as the first. See
   [Publishing ports](../../../apps/endpoints.md#publishing-ports).
2. Publish the `relay` TCP port.
3. Deploy the RustDesk app service again, so the server knows its public addresses.

**Show client settings** then also prints the ID server and relay server with their ports for these devices; their
**API server** stays empty. On other clusters the `id-udp` port gets a different number, and devices without
WebSocket can't sign in.

You don't need the `nat` port. Without it, the RustDesk app can't show which devices are online; sessions work normally.

## How sessions connect

Every session goes through the relay, and its traffic counts toward your cluster's bandwidth. Devices can't connect to
each other directly through Wodby's gateway.

The relay limits each session to 128 Mbit/s and all sessions together to 1024 Mbit/s. To change that, set the
`SINGLE_BANDWIDTH` and `TOTAL_BANDWIDTH` [environment variables](../../../apps/environment-variables.md) in Mbit/s, then
deploy the app service.

## Data

The `data` volume holds the server's key pair and its list of devices. If you lose the key pair, every device must be set
up again with the new key. The stack runs one replica.

If the app's domain changes, update the ID server and API server on every device.
