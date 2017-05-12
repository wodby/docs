# Using External Volumes on your Servers

If you want Wodby to use an external storage (mounted volume) instead of a server disk follow these steps:

1. Create a new volume for your server, e.g. Block Storage for DigitalOcean, EBS for AWS
2. Mount the volume to `/mnt/my-volume`. Instructions: [for DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-use-block-storage-on-digitalocean), [for AWS](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html) 
3. [Connect the server](../servers/connect/README.md) to Wodby if it's not already connected
4. Stop docker and kubernetes services (systemd):
```bash
$ service docker stop
$ service kube-* stop
```
5. Move docker's and Wodby's directories to the mounted volume and symlink them back:
```bash
$ mv /var/lib/docker /mnt/my-volume
$ mv /srv/wodby /mnt/my-volume
$ ln -s /mnt/my-volume/docker /var/lib/docker
$ ln -s /mnt/my-volume/wodby /srv/wodby
```
6. Start services
```bash
$ service docker start
$ service kube-* start
```
7. That's it, from now on applications' containers and their data will be stored on the mounted volume
