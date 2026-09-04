# Bitbucket

After connecting your Bitbucket account you can use its repositories as a build source for applications deployed via Wodby.

Wodby completes OAuth integration creation by asking you to select a Bitbucket workspace. The selected workspace is
stored as `BITBUCKET_WORKSPACE` and determines where Wodby discovers repositories.

## Build boilerplates

Bitbucket integrations can use Bitbucket repositories as app build sources. Automated import of public build boilerplates
into new Bitbucket repositories is not supported yet.

To start from a build boilerplate with Bitbucket, create or copy the repository manually in Bitbucket, then select that
repository as the build source in Wodby.
