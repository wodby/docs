# Using Private Docker Registry

If you store docker images from your stack in a private docker registry, you'll have to login to the registry from the server connected to Wodby. 

Connect to your server and execute the following commands (replace with your user and password) as root:

```bash
docker login -u<user> -p<password>
cp -R ~/.docker /
systemctl restart kube-apiserver
systemctl restart kube-controller
systemctl restart kube-kubelet
systemctl restart kube-proxy
systemctl restart kube-scheduler
```
