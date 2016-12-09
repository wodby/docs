# Connecting Custom Server

In case there's no native integration for your hosting provider, you can always connect your node by using feature "Custom server" regardless what hosting you're using:

1. Go to `My servers > Add`. Select `Custom server` and click proceed

2. You will see the page with requirements and instructions. Make sure all requirements are met 

3. Connect to your server by SSH and execute the agent installation command as a root. This command will download our agent which sets up the infrastructure and connects your server to our platform

4. Now you can deploy apps to this server

A few recommendations when connecting a custom server:

* Recommended minimum of server's RAM is 1GB
* We strongly recommend to avoid connecting working servers
* The following ports must be free: 80 (http), 443 (https), 31222-32222 (ssh)
