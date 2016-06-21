# Configuring git hooks for auto-deployment

This article explains how to configure git hooks to [enable auto-pull](../deployment/auto-deploy.md) for your app.

Please follow these instructions depending on your git provider:

## Custom git provider

1. Navigate to your git repo page in Wodby Dashboard and copy the auto-deployment webhook URL 
2. Connect to the server with your origin git repository
3. Go to `.git/hooks` directory and download there <a href="_files/post-receive.sh" target="_blank">`post-receive.sh`</a> file
4. Replace `<WEBHOOK URL>` in this file with the URL you copied before
5. Now let's make this file executable:
```bash
chmod +X post-receive
```
6. That's it!

## BitBucket

1. Navigate to your git repo page in Wodby Dashboard and copy the auto-deployment webhook URL
2. Open your repo page on BitBucket. Navigate to `Settings > Webhooks`. Click `Add webhook` button
3. Enter webhook title, paste the webhook URL you copied before to URL input and Save the form

## GitHub

1. Navigate to your git repo page in Wodby Dashboard and copy the auto-deployment webhook URL
2. Open your repo page on GitHub. Navigate to `Settings > Webhooks & services`. Click `Add webhook` button
3. Paste the webhook URL you copied before to Payload URL input and submit the form

## GitLab

1. Navigate to your git repo page in Wodby Dashboard and copy the auto-deployment webhook URL
2. Open your repo page on GitLab. Navigate to `Settings > Web Hooks`
3. Paste the webhook URL you copied before to URL input and submit the form

## AWS CodeCommit (coming soon)