# NetBird

The Wodby NetBird catalog stack runs a self-hosted [NetBird](https://netbird.io/) server: a WireGuard-based private
network that connects your devices and servers wherever they are. One app service runs the management server, sign-in,
the relay and the NetBird dashboard. The current composition is documented in
[`wodby/stack-netbird`](https://github.com/wodby/stack-netbird).

Everything runs over HTTPS, so it works on any cluster and you don't need to publish ports.

## Create the app

1. Create an app from the **NetBird** catalog stack.
2. Set the required **Admin email** and **Admin password** settings. The first deployment creates this administrator,
   so the dashboard never offers a public setup page.
3. Deploy. The first start downloads location databases used by posture checks and can take a few minutes before the
   app is ready.

Sign in to the dashboard at the app's main domain with the administrator's email and password. Changing the settings
later has no effect: change passwords, invite users and add single sign-on providers in the dashboard.

## Connect devices

1. In the dashboard, create a setup key under **Setup Keys**, or let people sign in from the NetBird client.
2. [Install the NetBird client](https://docs.netbird.io/get-started/install) on each device.
3. Point the client at your server's main domain:

    ```shell
    netbird up --management-url https://prod.myapp.example.com
    ```

    Add `--setup-key <key>` on devices without a browser. In the desktop apps, enter the same URL as the management URL
    in the settings.

Use the app's main domain as the management URL, the same address as the dashboard.

## Domains

The NetBird app service has two domains:

- The main domain of the `netbird` endpoint serves the dashboard and everything clients use to sign in and stay
  connected. Add your own domain to this endpoint if you want one.
- The `relay` endpoint has its own domain, `relay.<service>.<environment domain>`. The server tells clients about it;
  nobody enters it.

After you add a domain and make it primary for an endpoint, deploy the app service so the server uses the new address.
If the main domain changes, run `netbird up` with the new management URL on every device.

See [Endpoints](../../../apps/endpoints.md).

## How devices connect

Devices connect to each other directly when their networks allow it. To find their public addresses they use
Cloudflare's public STUN server (`stun:stun.cloudflare.com:3478`). NetBird's own STUN server isn't used: behind the
cluster's gateway it can't see the devices' addresses. To use other STUN servers, set the `NETBIRD_STUN_URIS`
[environment variable](../../../apps/environment-variables.md) to a space-separated list of `stun:` URLs, or to an
empty value for none, and deploy the app service.

When a direct connection isn't possible, traffic goes through the relay on your cluster, and it counts toward your
cluster's bandwidth.

## Data

The `data` volume holds the accounts, devices, network settings, users and activity log, in SQLite databases. If you
lose the volume, every device has to be set up again. The stack runs one replica.

Wodby generates the keys that encrypt sensitive data and sign-in sessions when the app is created. They stay the same
across deployments.
