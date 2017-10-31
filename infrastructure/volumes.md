# Using external volumes for applications data

If you want Wodby to use an external storage (mounted volume) instead of a server disk follow these steps:

#### 1. Creating new volume and attaching to server

See your cloud provider documentation

* [AWS](docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumes.html)
* [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-use-block-storage-on-digitalocean)
* ...

#### 2. Mounting volume
 
* Access your server and execute `sudo fdisk -l`. Find a device name (`/dev/NAME`) of your volume
* Create `ext4` file system on the new volume:
```bash
$ mkfs -t ext4 /dev/NAME
``` 
* Create a directory where you want to mount your volume:
```bash
$ mkdir /mnt/my-volume
```
* Mount your volume:
```bash
$ mount /dev/NAME /mnt/my-volume
``` 
* To mount this EBS volume on every system reboot, add an entry for the device to the `/etc/fstab` file:    
```bash
/dev/NAME /mnt/my-volume ext4 defaults,noatime 0 2
```

#### 3. Move docker and wodby's data to new volume

! THIS WILL CAUSE DOWNTIME OF ALL APPLICATIONS ON THE SERVER

* Stop docker and kubernetes services (systemd):
```bash
systemctl stop kube-apiserver
systemctl stop kube-controller
systemctl stop kube-kubelet
systemctl stop kube-proxy
systemctl stop kube-scheduler
systemctl stop docker
```
* Move docker's and Wodby's directories to your volume and symlink them back:
```bash
mv /var/lib/docker /mnt/my-volume
mv /srv/wodby /mnt/my-volume
ln -s /mnt/my-volume/docker /var/lib/docker
ln -s /mnt/my-volume/wodby /srv/wodby
```
* Start services
```bash
systemctl start docker
systemctl start kube-apiserver
systemctl start kube-controller
systemctl start kube-kubelet
systemctl start kube-proxy
systemctl start kube-scheduler
```

That's it, from now on applications-related data will be stored on the mounted volume
