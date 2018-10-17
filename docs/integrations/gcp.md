# Google Cloud Platform

## Connecting GCE virtual machine

Currently, we do not have a native integration with GCP. But you still can connect your server by following these steps:

0. Learn [requirements and recommendations](../infrastructure/connecting-server.md#requirements-and-recommendations)

1. Log in to GCP console with your account 

2. Create a new project if you don't have any

3. Navigate to the project page and click `Get started` under `Try Compute Engine` block
![](../assets/gcp-gce.png)

4. Once GCP prepare Compute Engine for your project, create a new virtual machine instance

5. Set VM instance attributes (list of [supported OS](../infrastructure/connecting-server.md#supported-os) and submit `Create` button
![](../assets/gcp-create-instance.png)

6. Navigate to a newly created instance page and find network link. Click on it
![](../assets/gcp-instance-network.png)

7. We need to add a new firewall rule for container ports 
![](../assets/gcp-firewall-rule.png)

8. Allow access for ports range 31222-32222 
![](../assets/gcp-rule-ports.png)

9. Now it's all set on GCP side. Now connect the server (`Servers > Connect > GCP`) and follow the instructions

!!! info "Root access"
    To gain root access you just need to run `sudo su` from your user