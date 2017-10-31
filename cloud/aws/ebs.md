# Mounting EBS volume to EC2 node

* Create new EBS volume and attach it to your EC2 instance as described in [AWS documentation](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumes.html)
* Access your EC2 instance as root and execute `fdisk -l`. Find a device name (`/dev/NAME`) of your volume
* Create `ext4` file system on the new volume:
```bash
$ mkfs -t ext4 /dev/NAME
``` 
* Create a directory where you want to mount your volume:
```bash
$ mkdir /mnt/ebs-100gb
```
* Mount your volume:
```bash
$ mount /dev/NAME /mnt/ebs-100gb
``` 
* To mount this EBS volume on every system reboot, add an entry for the device to the `/etc/fstab` file:    
```bash
/dev/NAME /mnt/new-100gb-ebs ext4 defaults,noatime 0 2
```    

If you want to increase an existing EBS volume please refer to [this article](https://www.elastic.co/blog/autoresize-ebs-root-volume-on-aws-amis). 