# Disk space management

Keep enough free space for container images, application data, temporary task
files, and the largest expected backup archive. Low disk space can make Docker,
containerd, kubelet, databases, and Wodby tasks fail in ways that are not fixed
merely by deleting one file.

!!! warning "After a full-disk incident"
    Do not immediately retry failed deployments or backups. Free space, inspect
    the runtime and application state, and restart only the affected component.
    If Kubernetes or container state is unclear, contact
    [Wodby support](../support.md) before deleting runtime data or rebooting.

## Check disk use

Start with filesystem and directory-level usage:

```shell
df -hT
du -xhd1 /srv/wodby
du -xhd1 /var/lib/docker
```

On Infrastructure 7, also inspect containerd and Docker's own accounting:

```shell
du -xhd1 /var/lib/containerd
docker system df
```

`ncdu` can provide an interactive view when it is available:

```shell
ncdu -x /srv/wodby
```

The main storage locations are:

- `/srv/wodby` — persistent application files and local backup archives;
- `/var/lib/docker` — Docker images, layers, containers, and volumes; and
- `/var/lib/containerd` — Infrastructure 7 containerd runtime data.

Never remove files directly from `/var/lib/docker` or `/var/lib/containerd`.
Those directories are runtime databases, not ordinary caches.

## Use an external volume

For a new server, attach and mount the external volume before connecting it to
Wodby. Use the provider's persistent filesystem identifier, such as a UUID, in
`/etc/fstab`; device names such as `/dev/sdb` can change after a reboot. Verify
the mount survives a reboot before deploying applications.

Moving an existing server's Wodby or container-runtime data requires downtime
and differs substantially by infrastructure generation. Infrastructure 7 uses
kubeadm, kubelet, Docker through cri-dockerd, and containerd; the old procedure
that stops separate `kube-apiserver`, `kube-controller`, or `kube-scheduler`
systemd units does not apply because its control plane runs as static Pods.

Contact support for a generation-specific migration procedure. Do not move or
symlink live runtime directories, use wildcard unmount commands, or copy them
while kubelet or a container runtime is writing to them.

## Reclaim space safely

### CI build images

Images stored in `registry.wodby.com` are managed from Wodby, not by deleting
files on the connected server. Use
[automatic build-image cleanup](../apps/deploy.md#automatically-clean-unused-build-images)
or delete an eligible historical build's images from `Instance > Builds`.
Registry usage and billing are updated asynchronously after deletion.

Local runtime image cleanup is infrastructure-specific. Infrastructure 6.0.4
and Infrastructure 5.7.7 or newer already include their legacy nightly Docker
cleanup. Do not add a duplicate cron job. On Infrastructure 7, review
`docker system df` and contact support before running a broad Docker prune;
removing an image needed by a stopped or pending workload can force a large
repull or prevent recovery while a registry is unavailable.

### Application and backup data

Deleting an instance removes its Wodby records and undeploys its workloads, but
persistent application and backup files can remain on a single-server host.
They are normally located beneath:

```text
/srv/wodby/instances/INSTANCE_UUID
/srv/wodby/backups/INSTANCE_UUID
```

Before removing retained data:

1. Confirm in the dashboard that the instance was deleted and will not be
   restored in place.
2. Verify the UUID against the deleted instance; do not identify data by a
   reused title or hostname.
3. Take a provider snapshot or copy any data that might still be needed.
4. Move the exact instance directories to a restricted quarantine location
   first.
5. Verify all remaining applications and backups before permanently deleting
   the quarantine copy.

Never use a wildcard or the whole `/srv/wodby` directory as a deletion target.
See [Deleting an instance](../apps/instances.md#deleting-an-instance) for the
control-plane resources removed by Wodby.

## Capacity planning

Use a dedicated data volume when possible and alert on both free bytes and free
inodes. Size it for live application data, retained backups, deployment layers,
temporary copies created during backup/restore, and expected growth. A 20–40 GB
system disk can be sufficient for a small host, but it is not a universal
capacity target for application data.
