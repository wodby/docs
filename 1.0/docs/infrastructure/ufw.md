# UFW configuration

The installer rejects an active UFW configuration because Docker and Kubernetes need forwarding and networking rules during installation. Temporarily disable UFW before connecting the server, then configure and re-enable it after installation.

Docker and Kubernetes forward container traffic. Set UFW's forwarding policy to `ACCEPT` in `/etc/default/ufw`:
 
Steps:

1. Edit the UFW configuration file, which is usually /etc/default/ufw or /etc/sysconfig/ufw. Set the DEFAULT_FORWARD_POLICY policy to ACCEPT.
```
DEFAULT_FORWARD_POLICY="ACCEPT"
```

Allow the server's actual SSH port before enabling UFW so you do not lock yourself out. Public Wodby traffic normally requires:

```shell
ufw allow ssh
ufw allow http
ufw allow https
ufw allow 31222:32222/tcp
```

The NodePort range is required only when an application exposes SSH or another service directly. Restrict it to trusted source networks whenever possible.

!!! danger "Do not expose control-plane ports"
    Do not create public rules for etcd ports 2379 or 4001, Kubernetes API port 6443, or kubelet port 10250. If a custom private network or firewall configuration requires one of these ports, restrict it to the exact trusted interface or source range.

Enable UFW:

```shell
ufw enable
```

Verify that application HTTP, HTTPS, and any required direct service ports work after enabling the firewall. UFW behavior can vary with provider firewalls and Docker's iptables rules; retain console access while testing.
