# Azure

## Connecting virtual machine

Currently, we don't have a native integration with Azure. But you still can connect your server by following these steps:

0. Learn [requirements and recommendations](../infrastructure/connecting-server.md#requirements-and-recommendations)

1. Login to Azure portal with your account

2. Click `Virtual Machines > Add`

3. Select OS from the list of [supported OS](../infrastructure/connecting-server.md#supported-os)

4. Enter the host name and the user name for your virtual machine. You will use this username later to access your server by SSH

5. Add your public key or the password to access later by SSH

6. Choose your pricing tier

7. On the step 3 choose `Network security groups` and create a new group

8. Besides the default SSH rule (port 22), add 3 additional rules for the following ports: 80 (HTTP), 443 (HTTPS), 31222-32222 (containers ports) as shown below: 

![](../assets/azure-network-security-groups.png)

9. Click create. Azure will spin up your new virtual machine

10. Optional but recommended: attach data disk as described [here](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/classic/attach-disk). Prepare directories to use the data disk:
    ```bash
    # If your data disk mounted to /mnt/data1
    mkdir -p /mnt/data1/wodby 
    mkdir -p /mnt/data1/docker
    ln -s /mnt/data1/wodby /srv/wodby
    ln -s /mnt/data1/docker /var/lib/docker    
    ``` 
    
11. Now it's all set on Azure's side. Now connect the server (`Servers > Connect > Microsoft Azure`) and follow the instructions

