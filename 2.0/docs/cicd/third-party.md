# Building with third-party CI

If you prefer to use your own CI system instead of the integrated [Wodby CI](wodby-ci.md), you can do so by using [Wodby CLI](../dev/cli.md).

The list of supported CI systems can be found [here](../integrations/types.md#cicd).

- To build your application with third-party CI, first you need to add a secret environment variable `WODBY_API_KEY` with your [API key](../dev/api-keys.md). 
- Next you need to add `$GIT_REPO_ID` environment variables, it's the ID of the git repository on Wodby that you've connected to the buildable app service. You can find it on the app service's Overview page
- Building with Wodby CLI is similar to building with Wodby CI, it consists of 4 steps:
    1. `wodby ci init $GIT_REPO_ID` - initializes the build process, fetch information about buildable app service and the stack, creates a build on Wodby with all information from your CI such as build number, id, git commit info 
    2. `wodby ci build [service]` - builds the specified service or all services if no service is specified. Optionally provide your own Dockerfile, custom tag and build context
    3. `wodby ci release` - pushes all the built images to associated [docker registry](docker-registry.md)
    4. `wodby ci deploy` - sends information about all built services to Wodby API, the build (that was created during init step) marked as complete and deployment of the build starts
