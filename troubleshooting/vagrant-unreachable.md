# Vagrant status is unreachable

When you turn off, restart or put to sleep your computer, Vagrant also turns off or sets on halt. In this case, you have to run Vagrant again by executing the following command in the directory with your Vagrant file:

```bash
$  vagrant up
```

Usually, it takes about `5 minutes` for Vagrant to start the machine. It can take longer (`up to 10 minutes` depending on the speed of your Internet connection) if Wodby needs to update the infrastructure.

Also, you will probably need to [remount the magic directory](../servers/connect/vagrant.md) again
