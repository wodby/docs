# Troubleshooting

## Cannot connect by SSH 

There are few known reasons for that:

* You must have at least one SSH key added to your profile
* Your ssh key not added to your SSH agent, try executing 
```shell
ssh-add /path/to/private/key
```
* Try specify which key to use 
```shell
ssh user@hostname -i /path/to/private/key`
```

## Emails delivery from my application fails

If you're using a server from a public cloud there's 90% chance that its IP is already compromised and blacklisted by major mail services, hence your emails won't be delivered or will land in the spam folder.

If your stack has mail transfer agent OpenSMTPD we recommend integrating it with a 3rd party email service (relay mode):

* [AWS Simple Email Service](integrations/aws.md)
* [SendGrid](integrations/sendgrid.md)
* Any other SMTP server, see OpenSMTPD stack documentation
 
## Host identification has changed

If you see the following error:

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
@ WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED! @ 
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY! 
Someone could be eavesdropping on you right now (man-in-the-middle attack)! 
It is also possible that a host key has just been changed. 
The fingerprint for the RSA key sent by the remote host is 
SHA256:XXXXXXXXXXXXX/XXXX. 
Please contact your system administrator. 
Add correct host key in /Users/xxx/.ssh/known_hosts to get rid of this message. 
Offending RSA key in /Users/xxx/.ssh/known_hosts:xx 
RSA host key for [node-xxxxx.wod.by]:xxxx has changed and you have requested strict checking. 
Host key verification failed.
```

This means that the container you're trying connect to was recreated and RSA key has changed.

To avoid this kind of errors you can disable strict host key checking for *.wod.by host by adding the following lines to `~/.ssh/config` file: 

```
Host *.wod.by
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
```

## My server status is unreachable

This problem could be caused by the lack of memory on your server. Make sure you have enough memory:

```shell
free -m
```

If you don't have enough memory, you can use Linux Swap.

Make sure you're using swap by executing:
```shell
sudo swapon -s
```
If not, follow [this guide](https://www.digitalocean.com/community/tutorials/how-to-add-swap-on-ubuntu-12-04") to add swap (Ubuntu).

Also, the N/A status may be caused by a hanged wodby agent container, see [how you can restart it](infrastructure/cli.md#restarting-wodby-agent).

If you still have the problem please contact Wodby support team.

## Cannot connect server

There are few known reasons for that:

* Make sure your server satisfies [requirements and recommendations](infrastructure/index.md)
* Wodby's script must be run as a root
* A slow speed of Read/Write operations on a disk. See [the list](infrastructure/index.md) of recommended hosting providers
* [Docker requirements](https://docs.docker.com/engine/installation/binaries/) are not met 
* [ufw enabled](infrastructure/ufw.md)
* Inbound / outbound external firewall
* Non-compatible virtualization (virtuozza)

## Application deployment or other tasks fail

This error means that one of the deployment steps exceeded its timeout. There are few known reasons for that:

* There's something wrong on our side, see http://status.wodby.com/
* Something wrong with your server, make sure you have enough [free disk space](infrastructure/disk.md)
* Check your CPU load average by running top
* Check you have enough free RAM by running free -h
* Check your system log for extra errors journalctl -f 
* You've reached containers limit per server (300), contact our support to increase the limit
* A slow speed of Read/Write operations on a disk
* Huge ping to your server due to global network issues

## Application gives "File not found" error

This error means that the HTTP server could not find the entrypoint (in case of PHP-based stacks it's usually `index.php`) in a container. This might happen for a few reasons:

* You have your entrypoint (e.g. `index.php`) in a subdirectory of your git root and you did not specify it during the initial deployment of new application
* Your codebase is missing, could be that you've selected a wrong branch during deployment/build

## Cannot update WordPress core or its plugins/themes

See [this article](stacks/wordpress/index.md#upgrading-wordpress)

## Infrastructure 5.x known issues

* Sometimes we can't get logs of a task with the error `Container not found`. Task may have been completed but we consider it as failed
* Sometimes we can't get the size of a backup archive so we don't show it in the dashboard
* If you update a [ rolling-update](stacks/template.md#deployment) container and it fails we will not be able to detect the failure. Despite the actual failure the deployment will be considered successful because the older version of the container is still intact
* We can not handle errors of containers that failed to start, so the task will hang until it expires by timeout. Here's how you can manually check your deployment state in such cases:    
    1. Access your server via SSH as root
    2. Run the following command (replace `[INSTANCE UUID]`)
        ```shell
        kubectl get po -n [INSTANCE UUID]
        ``` 
    3. You will see statuses of pods (containers) of your application instance. You can get logs of the specific pod (container) either by running (if container is creating or running)
        ```shell
        kubectl logs [POD NAME] -n [INSTANCE UUID]
        ```
        or (if container is not currently running or in the error state)
        ```shell
        kubectl describe po [POD NAME] -n [INSTANCE UUID]
        ```

!!! info "Infrastructure 6.x"
    All the known issues will be resolved in Infrastructure 6.x
    
## Permissions denied error on static files

This usually happens when public files owned by a user with UID/GID different from an HTTP server user and have no reading permissions for others, e.g. `-rwxr-x---` or `750`. To give the writing permissions for others you'll have to executing the following commands from the host server as root (most likely you won't be able to do it from a different user):
```
chmod -R o=rX /srv/wodby/instances/[APP INSTANCE UUID]/files/public/
```  
