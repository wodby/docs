# UFW configuration

If you want to use ufw (uncomplicated firewall) on a server connected to Wodby, you’ll need to do additional configuration. Docker uses a bridge to manage container networking. By default, UFW drops all forwarding traffic. You must set UFW’s forwarding policy appropriately.
 
Steps:

1. Edit the UFW configuration file, which is usually /etc/default/ufw or /etc/sysconfig/ufw. Set the DEFAULT_FORWARD_POLICY policy to ACCEPT.

```
DEFAULT_FORWARD_POLICY="ACCEPT"
```

Save and close the file.

2. Allow allow rule for port 4001 (etcd):

```bash
$ ufw allow 4001/tcp
```

3. Reload UFW. 

```bash
$ sudo ufw reload
```