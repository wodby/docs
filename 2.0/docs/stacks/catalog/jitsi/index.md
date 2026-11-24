---
description: Run Jitsi Meet video meetings on Wodby with the Jitsi Meet catalog stack, with a moderator account, guest access and a published media port.
---

# Jitsi Meet stack guide

The Wodby Jitsi Meet catalog stack runs [Jitsi Meet](https://jitsi.org/jitsi-meet/) video meetings. The current
composition is documented in [`wodby/stack-jitsi`](https://github.com/wodby/stack-jitsi).

The stack needs no repository: Jitsi Meet runs from its own images.

## Before you create the app

- The cluster must be able to publish UDP ports. See [Publishing ports](../../../apps/endpoints.md#publishing-ports).
- Audio and video go straight from each participant's browser to a published UDP port on the cluster. Participants
  whose network blocks outgoing UDP traffic can join a meeting and chat, but they get no audio or video.
- The Jitsi Meet service requests about 0.8 GiB of memory. Calls need more CPU as participants join; give the service
  more CPU for larger meetings.

## Moderator account and guests

Set the moderator in the Jitsi Meet service's settings when you create the app:

| Setting | Default | What it sets |
| --- | --- | --- |
| **Moderator username** | `moderator` | The username that signs in to start meetings |
| **Moderator password** | none, required | The moderator's password |
| **Allow guests** | `1` | `1` lets anyone with a meeting link join once the moderator has started the meeting. `0` makes everyone sign in |
| **Media IP address** | empty | The public IPv4 address browsers send audio and video to. Leave it empty unless your domain goes through a proxy; see [Domains behind a proxy](#domains-behind-a-proxy) |

Jitsi Meet keeps only this account. To change its password, change **Moderator password** and deploy the Jitsi Meet
service again.

## Publish the media port

After the app is created:

1. Open **Apps > [App] > [Environment] > Endpoints > Ports**, select the `jitsi` endpoint, and publish the `media` UDP
   port. See [Publishing ports](../../../apps/endpoints.md#publishing-ports).
2. Deploy the Jitsi Meet service again, so it tells browsers the new port.

Without a published media port, meetings start but carry no audio or video. If you unpublish the port or it gets a new
number, deploy the service again.

## Start a meeting

1. Open the app's main domain, enter a meeting name and select **Start meeting**.
2. When Jitsi Meet shows **Waiting for a moderator…**, select **Log-in** and sign in with **Moderator username** and
   **Moderator password**.
3. Share the meeting link. With **Allow guests** on, people who open the link wait until the moderator has joined, then
   enter the meeting.

## Domains behind a proxy

Browsers send audio and video to the address your app's domain points to. If the domain goes through a proxy, such as
Cloudflare with proxying turned on, it points to the proxy instead, and meetings have no audio or video. Set
**Media IP address** to the cluster's public IP and deploy the Jitsi Meet service again.

## Updates

Jitsi Meet updates arrive with new revisions of the Jitsi Meet service. Deploying the service ends the meetings in
progress, so deploy when no meetings are running.

## Data

Meetings are not stored, so the app has nothing to back up.

## Troubleshooting

If participants see and hear nothing, check the Jitsi Meet service's logs for one of these messages:

- `the media port isn't published`: publish the `media` port and deploy again.
- `doesn't resolve to an IPv4 address`: set **Media IP address** and deploy again.

If the logs show `Browsers send audio and video to <IP>:<port>` with the right IP and port, make sure the participants'
network allows outgoing UDP traffic to that port.

## Limits

- One instance of the service carries every meeting; the number of participants is limited by its CPU.
- No relay for networks that block UDP.
- No recording, live streaming, phone dial-in or transcription.
- Sign-in uses the single moderator account; other sign-in methods aren't supported.
