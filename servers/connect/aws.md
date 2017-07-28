# Connecting EC2 Node from AWS

Currently, we don't have a native integration with AWS. But you still can connect your server by following these steps: 

1. Login to your AWS Console 
2. Choose EC2 (Virtual Servers in the Cloud)
3. Choose `Instances > Click "Launch Instance"`
4. Choose an image (AMI) from the list of [supported OS](../supported-os.md)
5. Choose an instance type. **Do not** use `t2` (burstable performance) instances unless you know what you're doing
6. Go to `4. Add Storage` (vertical tabs) and set `Size (GiB)` to at least `20`
7. Go to `6. Configure Security Group`. Besides the default SSH rule (port 22), add the following rules: HTTP, HTTPS and custom TCP rule with the range 31222-32222 as shown below:
![](_images/aws-security-groups.png)
8. Click `Review and Launch`
9. Now it's all set on AWS side. Now connect the server (`Servers > Connect > AWS`) and follow the instructions
