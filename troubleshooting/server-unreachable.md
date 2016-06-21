# My server status is unreachable

This problem could be caused by the lack of memory on your server. Make sure you have enough memory:

```
$ free -m
```

If you don't have enough memory, you can use Linux Swap.

Make sure you're using swap by executing:
```
$ sudo swapon -s
```
If not, follow <a href="https://www.digitalocean.com/community/tutorials/how-to-add-swap-on-ubuntu-12-04" target="_blank">this guide</a> to add swap (Ubuntu).

If you still have the problem please contact Wodby support team.
