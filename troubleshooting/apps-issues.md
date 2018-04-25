# My application deployed via Wodby doesn't work

* Disk space is out: df -h. Must reboot after clearing space
* AWS, Azure, GCP: check if ports (http/https) are open
* [ufw enabled](/infrastructure/ufw.html)
* [Cloudflare is being used](/infrastructure/cloudflare.html)
* Containers limit (300) exceeded, contact Wodby support
* Server is not powerful enough for so many containers. See CPU load average via `top` , see `journalctl` logs
* No free memory / swap: `free -h`
* Network issues: is etcd reachable from agent, edge, dns
* SE Linux / AppArmor related issues
