---
description: Connect a GitHub repository to Wodby 1 and add a webhook so that pushes to a branch deploy your application automatically.
---

# GitHub integration

## Connecting repository

* Connect your GitHub account by adding a new integration
* Navigate `My repos > Connect`, select `GitHub` and your integration
* Click `Proceed`. Now select the repository you'd like to connect

## Add git hook for auto-deployment

* Navigate to your git repository page in Wodby Dashboard and copy the auto-deployment `Webhook URL`
* Open your repo page on GitHub. Navigate to `Settings > Webhooks & services`. Click `Add webhook` button
* Paste the URL you copied before to `Payload URL` input and submit the form
