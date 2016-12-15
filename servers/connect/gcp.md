# Connecting Virtual Machine from Google Cloud Platform (GCP)

Currently, we don't have a native integration with GCP. But you still can connect your server by following these steps:

1. Log in to <a href="http://cloud.google.com/" target="_blank">GCP</a> with your account 

2. Create a new project if you don't have any

3. Navigate to the project page and click `Get started` under `Try Compute Engine` block
<hr>![](_images/gcp-gce.png)<hr>

4. Once GCP prepare Compute Engine for your project, create a new virtual machine instance

5. Set VM instance attributes and submit `Create` button
<hr>![](_images/gcp-create-instance.png)<hr>

6. Navigate to a newly created instance page and find network link. Click on it
<hr>![](_images/gcp-instance-network.png)<hr>

7. We need to add a new firewall rule for container ports 
<hr>![](_images/gcp-firewall-rule.png)<hr>

8. Allow access for ports range 31222-32222 
<hr>![](_images/gcp-rule-ports.png)<hr>

9. Now it's all set on GCP side. Now connect the server (`Servers > Connect > GCP`) and follow the instructions