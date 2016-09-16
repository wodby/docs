# Connecting Git Repository from BitBucket

1. Connect your BitBucket account by adding a [new integration](../../integrations/README.md)

2. Navigate `My repos > Connect`, select BitBucket and your integration

3. Click `Proceed`. Now select the repository you'd like to connect 

4. Great! Now you can create/import new apps using your git repo

If you want to use [remote workspace](../../apps/remote-workspace/README.md) you should grant Wodby writable access to your repository. However BitBucket doesn't support writable deployment keys so there's a quick workaround for that: 

* Open git repository page from the Wodby dashboard and copy the public key

* Add copied key either to your BitBucket account (`Profile > BitBucket settings > SSH Keys`) or create a separate user for Wodby
 
* Now you should be able to commit changes using remote workspace
