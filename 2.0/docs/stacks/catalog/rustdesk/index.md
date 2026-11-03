# RustDesk Server

The Wodby RustDesk Server catalog stack runs the open-source [RustDesk](https://rustdesk.com/) server, so your devices
use your own server for remote desktop sessions instead of RustDesk's public one. The current composition is documented
in [`wodby/stack-rustdesk`](https://github.com/wodby/stack-rustdesk).

The open-source server has no web interface: you use it from the RustDesk app on each device. The app's domain shows a
page with the server's address and these setup steps.

## Before you create the app

RustDesk devices sign in over UDP and connect over TCP on the same address and port, so the server needs a TCP port and a
UDP port published on the same public port number. Wodby supports that on [K3S](../../../clusters/k3s.md) clusters and
[single-node clusters](../../../clusters/managed.md#single-node-clusters). On other clusters, the UDP port gets a different
number and devices can't sign in.

## Publish the server's ports

1. Create an app from the **RustDesk Server** catalog stack and deploy it.
2. Open **Apps > [App] > [Environment] > Endpoints > Ports**, select the `rustdesk` endpoint, and publish the `id` TCP
   port, then the `id-udp` UDP port. The second one gets the same public port as the first. See
   [Publishing ports](../../../apps/endpoints.md#publishing-ports).
3. Publish the `relay` TCP port.
4. Deploy the RustDesk app service again, so the server knows its public addresses.

You don't need the `nat` port. Without it, the RustDesk app can't show which devices are online; sessions work normally.

## Set up devices

1. On the RustDesk app service, run the **Show client settings** action. See [Actions](../../../apps/services.md#actions).
   The task log shows the values to enter.
2. In the RustDesk app on each device, open **Settings > Network > ID/Relay server** and enter the **ID server**,
   **Relay server** and **Key** from the task log. Leave **API server** empty.

The ID server and relay server use the app's main domain with the published ports, for example
`prod.myapp.example.com:31222`. The key is the server's public key: devices without it can't use the server, so share it
only with people who should use your server.

You don't need **Use WebSocket**. Devices with it turned on can connect to other devices, but no one can connect to them,
because the open-source server signs devices in only over UDP.

## How sessions connect

Wodby's gateway hides each device's own address from the server, so devices can't connect to each other directly. Every
session goes through the relay, and its traffic counts toward your cluster's bandwidth.

The relay limits each session to 128 Mbit/s and all sessions together to 1024 Mbit/s. To change that, set the
`SINGLE_BANDWIDTH` and `TOTAL_BANDWIDTH` [environment variables](../../../apps/environment-variables.md) in Mbit/s, then
deploy the app service.

The server limits how many devices can sign in from one address, and here all devices reach it through the gateway's
address. That suits up to a few hundred devices.

## Data

The `data` volume holds the server's key pair and its list of devices. If you lose the key pair, every device must be set
up again with the new key. The stack runs one replica.

If you publish the ports again and they get different numbers, deploy the app service and update the addresses on every
device.
