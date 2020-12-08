# Disk space management

!!! failure "Recovery after out of disk space"
    If your server did not have enough disk space to properly operate we highly encourage your to reboot the server as the state of some infrastructure components may be corrupted

## Using external volumes for applications data

If you want Wodby to use an external storage (mounted volume) instead of a server disk follow these steps:

### 1. Creating new volume and attaching to server

See your cloud provider documentation

* [AWS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumes.html)
* [DigitalOcean](https://www.digitalocean.com/docs/volumes/how-to)
* ...

### 2. Mounting volume
 
* Access your server and execute `sudo fdisk -l`. Find a device name (`/dev/NAME`) of your volume
* Create `ext4` file system on the new volume:
```shell
mkfs -t ext4 /dev/NAME
``` 
* Create a directory where you want to mount your volume:
```shell
mkdir /mnt/my-volume
```
* Mount your volume:
```shell
mount /dev/NAME /mnt/my-volume
``` 
* To mount this EBS volume on every system reboot, add an entry for the device to the `/etc/fstab` file:    
```shell
/dev/NAME /mnt/my-volume ext4 defaults,noatime 0 2
```

### 3. Moving docker and wodby's data to new volume

!!! danger "Downtime" 
    This action will cause downtime of all applications on the server

1\. Stop docker and kubernetes services (systemd):

```shell
systemctl stop kube-apiserver
systemctl stop kube-controller
systemctl stop kube-kubelet
systemctl stop kube-proxy
systemctl stop kube-scheduler
systemctl stop docker
```

!!! warning "Some containers don't react to SIGTERM" 
    Some processes (e.g. crond, node) might ignore `SIGTERM` signal received when you stop docker daemon and still running, that might prevent you from moving directories in the next step because some containers mounts are still in use (device busy errors). You might need to `kill` those processes manually and unmount containers directories:
    ```shell
    umount /var/lib/docker/overlay2/*/merged
    umount /var/lib/docker/containers/*/shm
    ```  

2\. Move docker's and Wodby's directories to your volume and symlink them back:

```shell
mv /var/lib/docker /mnt/my-volume
mv /srv/wodby /mnt/my-volume
ln -s /mnt/my-volume/docker /var/lib/docker
ln -s /mnt/my-volume/wodby /srv/wodby
```

3\. Start services

```shell
systemctl start docker
systemctl start kube-apiserver
systemctl start kube-controller
systemctl start kube-kubelet
systemctl start kube-proxy
systemctl start kube-scheduler
```

That's it, from now on applications-related data will be stored on the mounted volume

## Freeing disk space

We recommend connecting servers with at least 20-40G of disk space and using a separate volumes for your applications data. 

### Checking disk space

You can check if you have enough disk space on your server by running:

```shell
df -h
```

If you want to learn what exactly on your server takes disk space, you can run:

```shell
du -sh /path/to/directory/*
```

Or using a tool called ncdu 

```shell
apt-get install ncdu
ncdu /path/to/dir
```

### What can I clean up?

The most heavy directories are usually:

* `​/srv/wodby` – contains persistent files of your applications and backups. Read below how to clean it up
* `​/var/lib/docker` – docker's volumes, containers, images data. Do not clean it up

#### Clean up docker's unused images form previous builds

```shell
docker system prune -a
```

!!! info "Crontab already configured"
    Since infrastructure version [5.7.7](maintenance.md) the following crontab line already included.

You can add this command to your server cron to execute automatically. Run `crontab -e` on your server and add the following line (run every night at 2:30am):
```shell
30 2 * * * /usr/bin/docker system prune -af
```

#### Backups

You can delete old backups of your applications by using the following path:
```shell
/srv/wodby/backups/[INSTANCE_UUID]
```

#### Deleting application instances files

!!! warning "Infrastructure 5.x"
    The following applies only for single-server infrastructure version 5.x
​
When you delete an instance Wodby does not delete containers' persistent files (database, codebase, etc) on your server to ensure no valuable data will be lost. Please follow the instructions below to clean up your server from these outdated files:

1. Move outdated files to a separate directory
```shell
docker run --rm -it -v /srv/wodby:/srv/wodby wodby/cleanup 'API Token'
```
2. Make sure your applications still operate correctly. Delete outdated files
```shell
rm -rf /srv/wodby/_deleted
```
