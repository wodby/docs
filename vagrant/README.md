# Vagrant

## Connecting your local machine via Vagrant

Wodby allows you to connect your local machine using Vagrant. Vagrant machine is personal for every user and not available to other users from the same organization. You will be able to deploy new apps and apps local instance to Vagrant.

Follow these steps to connect your local machine:

1. Download and install <a href="https://www.virtualbox.org/" target="_blank">VirtualBox</a> + <a href="https://www.vagrantup.com/" target="_blank">Vagrant</a> if you don't have it yet

2. Go to `Servers > Connect` page, choose Vagrant and click proceed

3. Choose your OS and click Proceed

4. Follow the instructions on this page

## Mounting magic directory

If you accidentally unmounted the magic directory from your Vagrant, you can remount it manually using the following commands (replace `[VAGRANT_IP]` with IP of your Vagrant machine, you can find it on a servers list page).

For OS X 
```bash
$ mkdir ./wodby && sudo mount_nfs -o resvport [VAGRANT_IP]:/srv/wodby/usr ./wodby
```

For Linux:
```bash
$ mkdir ./wodby && sudo mount [VAGRANT_IP]:/srv/wodby/usr ./wodby
```

On some linux systems you also might need to install `nfs-common` package.