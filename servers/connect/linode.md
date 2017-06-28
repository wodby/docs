# Connecting Linode

**Debian 8 provided by Linode is not compatible (because of custom kernel), please use Ubuntu instead**

Currently, we don't have a native integration with Linode. But you still can connect your server by following these steps: 

1. Login to <a href="https://manager.linode.com/" target="_blank">Linode manager</a> 

2. Spin up a new linode
<br>![](_images/linode-add-new.png)

3. Wait for linode being created. Once its status is set to "Brand New". Navigate to this linode dashboard
<br>![](_images/linodes.png)

4. Click "Deploy an image"
<br>![](_images/linode-deploy-image.png)

5. Choose image attributes (list of [supported OS](../supported-os.md)) and deploy
<br>![](_images/linode-image-attributes.png)

6. Wait until all disks are create and boot the linode
<br>![](_images/linode-boot.png)

7. Now it's all set on Linode's side. Now connect the server (`Servers > Connect > Linode`) and follow the instructions