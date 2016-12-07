# UFW configuration

If you want to use ufw (uncomplicated firewall) on a server connected to Wodby, you’ll need to do additional configuration. Docker uses a bridge to manage container networking. By default, UFW drops all forwarding traffic. You must set UFW’s forwarding policy appropriately.
 
Steps:

1. Enable ufw
```bash
$ ufw enable
```

2. Edit the UFW configuration file, which is usually /etc/default/ufw or /etc/sysconfig/ufw. Set the DEFAULT_FORWARD_POLICY policy to ACCEPT.
```
DEFAULT_FORWARD_POLICY="ACCEPT"
```

3. Add following rules:
```bash
$ ufw allow ssh
$ ufw allow http
$ ufw allow https
$ ufw allow 31222:32222/tcp
$ ufw allow 4001/tcp
$ ufw allow 6443/tcp
```

4. Reload UFW:
```bash
$ ufw reload
```