# Host identification has changed

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

This means that the container you're trying connect to was rebooted and RSA key has changed.

To avoid this kind of errors you can disable strict host key checking for *.wod.by host by adding the following lines to `~/.ssh/config` file: 

```
Host *.wod.by
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
```