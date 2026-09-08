# Troubleshooting

## Cannot connect by SSH

Check the following:

- At least one SSH public key is added to your Wodby profile.
- The corresponding private key is loaded in your SSH agent:

    ```shell
    ssh-add /path/to/private/key
    ```

- If you have several keys, select the expected key explicitly:

    ```shell
    ssh -i /path/to/private/key user@hostname
    ```

See the instance or server page for the current host, port, and username.

## Remote host identification changed

SSH stops when the key presented by a host no longer matches its entry in
`known_hosts`. A legitimately recreated container or server can have a new key,
but the same warning can also indicate that you reached the wrong host or that
the connection is being intercepted.

1. Confirm that the hostname and port still belong to the intended Wodby
   instance or server.
2. Verify the new fingerprint through a trusted channel, such as the server
   provider's console or Wodby support.
3. Remove only the stale entry:

    ```shell
    ssh-keygen -R hostname
    ```

   For a non-standard port, use:

    ```shell
    ssh-keygen -R '[hostname]:port'
    ```

4. Reconnect, compare the displayed fingerprint with the verified value, and
   accept it only when they match.

Do not disable strict host-key checking globally or discard all entries for
`*.wodby.cloud`.

## Email delivery fails

Public-cloud IP addresses often have little or poor mail reputation, so direct
mail can be rejected or classified as spam. Use OpenSMTPD in relay mode with a
reputable SMTP provider:

- [AWS Simple Email Service](integrations/aws.md)
- [SendGrid](integrations/sendgrid.md)
- another SMTP service supported by your OpenSMTPD configuration

See [Mail delivery](infrastructure/mail-delivery.md).

## Server status is unreachable

Check host capacity and service health:

```shell
free -h
df -h
top
```

Infrastructure 7 disables swap; adding swap is not a supported remedy for an
unreachable server. Reduce resource pressure or increase the server's RAM or
disk capacity instead.

An unresponsive Wodby Agent can also produce an `N/A` status. Use the commands
for your infrastructure generation under
[Restart Wodby Agent](infrastructure/cli.md#restart-wodby-agent), then inspect
its logs before restarting other services. If the server remains unreachable,
contact [Wodby support](support.md).

## Cannot connect a server

Check the following before running the generated installer command again:

- The host satisfies the
  [Infrastructure 7 requirements](infrastructure/connecting-server.md#infrastructure-7-requirements).
- The generated installer command is run as `root`.
- Docker, Kubernetes, containerd, and CNI software are not already installed.
- UFW was handled as described in [UFW](infrastructure/ufw.md).
- External firewalls allow the required inbound and outbound traffic.
- The host does not use unsupported virtualization such as OpenVZ.
- Disk and network performance are sufficient for installation.

## Deployment or another task times out

`Operation exceeded timeout` means the backend did not receive a terminal
result before its deadline. It does **not** prove that the server-side command
or Kubernetes operation failed. The operation can still be running or may have
completed after the connection was interrupted.

Before retrying:

1. Read the complete task log and note the last action sent to the server.
2. Check [Wodby status](https://status.wodby.com/) and the connected server's
   reachability, free disk, memory, CPU load, and network latency.
3. Inspect the application's current external state. On Infrastructure 7:

    ```shell
    kubectl get pods -n INSTANCE_UUID -o wide
    kubectl describe pod -n INSTANCE_UUID POD_NAME
    kubectl logs -n INSTANCE_UUID POD_NAME --all-containers --tail=200
    ```

4. Retry only after establishing whether the previous operation took effect.
   Repeating a create, restore, migration, or deployment blindly can duplicate
   work or apply it to an already changed application.

If the external state is unclear, preserve the task log and contact support
instead of deleting Pods, purging queues, or restarting the whole server.

Other common causes include insufficient disk or memory, high CPU or disk I/O,
very high network latency, and reaching the recommended container capacity of
the server.

## Application reports "File not found"

The HTTP service could not find the configured entry point, such as `index.php`
for many PHP stacks. Verify that:

- the application document root points to the directory containing the entry
  point; and
- the selected repository branch and latest deployment contain the expected
  code.

## Permission denied for static files

This usually means the files are owned by a different UID/GID and are not
readable by the HTTP-service user. Inspect the ownership and permissions before
changing them. On a single-server installation, the following grants read and
directory traversal permission to other users without making files writable:

```shell
chmod -R o=rX /srv/wodby/instances/INSTANCE_UUID/files/public/
```

Apply it only to the verified instance path. If the stack expects a different
ownership model, use its documented permission helper instead.

## Backup failures

Common causes include:

- insufficient free disk space for both the live data and archive;
- less than approximately 256 MB of free memory;
- high CPU or disk-I/O utilization;
- an unreachable server or failed database/file service; and
- invalid or expired mirror-storage credentials.

Inspect the failed task and the specific overdue component reported by Wodby.
Schedule large automatic backups during a low-traffic period and see
[Backups](apps/backups.md) for component schedules and retention behavior.

## Cannot update WordPress core, plugins, or themes

See [Upgrading WordPress](stacks/wordpress/index.md#upgrading-wordpress).
