# Using Remote Workspace via SSHFS

## Instructions for Linux

* Install SSHFS and add your user to the new group
```
$ sudo apt-get install sshfs
$ sudo gpasswd -a "$USER" fuse
```

* Sign out / sign in to apply a new group

* Create a directory where you want to mount 

* Navigate to `[Instance] > Stack > [Backend]` and copy the `SSHFS command`

* In the command replace token `%dir%` with the directory you has created
  
* Execute the command to mount the remote docroot to your local machine

* You can always unmount the directory later by using the following command:
```
$ fusermount -u %dir%
```


## Instructions for OS X

* Download and install the latest version of `FUSE for OS X` and `SSHFS` from http://osxfuse.github.io/

* Create a directory where you want to mount 

* Navigate to `[Instance] > Stack > [Backend]` and copy the `SSHFS command`

* In the command replace token `%dir%` with the directory you has created
  
* Execute the command to mount the remote docroot to your local machine

* You can always unmount the directory later by using the following command:
```
$ umount %dir%
```
