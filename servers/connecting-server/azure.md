# Connecting a server from MS Azure

Currently, we don't have a native integration with Azure. But you still can connect your server by following these steps:

1. Login to <a href="https://portal.azure.com/" target="_blank">Azure portal</a> with your account

2. Click `Virtual Machines > Add`

3. Select OS (use search to make it faster)

4. Enter the host name and the user name for your virtual machine. You will use this username later to access your server by SSH

5. Add your public key or the password to access later by SSH

6. Choose your pricing tier

7. On the step 3 choose `Network security groups` and create a new group

8. Besides the default SSH rule (port 22), add 3 additional rules for the following ports: 80 (HTTP), 443 (HTTPS), 31222-32222 (containers ports) as shown below: 
<br>![](_images/azure-network-security-groups.png)

9. Click create. Azure will spin up your new virtual machine

10. Now it's all set on Azure's side. Now connect the server (`Servers > Connect > Microsoft Azure`) and follow the instructions

