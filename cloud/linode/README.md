# Manual connection of Linode server

Currently, we don't have a native integration with Linode. But you still can connect your server by following these steps: 

1. Login to [Linode manager](https://manager.linode.com) 

2. Spin up a new linode
<br>![](_images/linode-add-new.png)

3. Wait for linode being created. Once its status is set to "Brand New". Navigate to this linode dashboard
<br>![](_images/linodes.png)

4. Click "Deploy an image"
<br>![](_images/linode-deploy-image.png)

5. By default Linode uses a custom Linux Kernel version, we should replace it to the Kernel version that comes with the Linux distribution. Click Edit to view a distribution’s configuration profile options as shown below and change Kernel to `GRUB2`:
<br>![](_images/linode-image-edit.png)
<br>![](_images/linode-kernel.png)

6. Choose image attributes (list of [supported OS](/servers/supported-os.md)) and deploy
<br>![](_images/linode-image-attributes.png)

7. Wait until all disks are create and boot the linode
<br>![](_images/linode-boot.png)

8. Now it's all set on Linode's side. Now connect the server (`Servers > Connect > Linode`) and follow the instructions