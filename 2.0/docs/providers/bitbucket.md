# Bitbucket

After connecting your Bitbucket account you can use its repositories as a build source for applications deployed via Wodby.

Wodby completes OAuth integration creation by asking you to select a Bitbucket workspace. The selected workspace is
stored as `BITBUCKET_WORKSPACE` and determines where Wodby discovers repositories.

## Build boilerplates

Wodby can't create repositories on Bitbucket, so you create the repository first. Wodby copies the boilerplate into it
at the app's first deployment.

1. In the integration's workspace on Bitbucket, create an empty repository, without a README or `.gitignore`.
2. In Wodby, choose **Clone boilerplate**, select the Bitbucket integration, and enter the repository's name as it
   appears in its URL. Names can use letters, digits, dots, dashes, and underscores.

If the repository doesn't exist or already has commits, Wodby stops before creating the app and tells you what to fix.

The connected Bitbucket account needs write access to the repository; without it, the app is created but its first
deployment fails. For pushes to start builds, the account also needs the **Admin** permission on the repository. Without
it, the deployment continues and its log warns you. If you connected the integration before Wodby supported Bitbucket
webhooks, reconnect it once.

Wodby builds from the boilerplate's branch. If the repository's main branch is a different one, the deployment continues
and its log warns you. You can change the main branch in the repository settings on Bitbucket.

To build from a repository that already has code, select it as the build source instead.
