---
description: Deploy a React application on Wodby with the React catalog stack, which builds the app in the pipeline and serves it with Nginx.
---

# React

The Wodby React catalog stack serves a built React application with Nginx. The current service and defaults are
documented in [`wodby/stack-react`](https://github.com/wodby/stack-react).

## Build and deployment

Start from the [React boilerplate](https://github.com/wodby/react-boilerplate) or connect your own repository. The
deployed app service runs no Node.js process. The pipeline installs dependencies, runs the production build, and builds
the image from the output directory only (`dist` in the boilerplate). Source files and `node_modules` are not in the
image.

If you change the name or location of the build output, change the pipeline's `wodby ci build --from` step too.
Otherwise the image is built from the wrong directory. See [Application Builds](../../../apps/builds.md).

Nginx answers requests for paths that are not files with `index.html`, so client-side routes work without extra
configuration. `/.healthz` returns status 204.

## Configuration reaches the build, not the browser

The application runs in the browser. Environment variables of the app service, including `WODBY_*`, do not reach it at
run time. Put the values it needs into the build, or have the application fetch them from an API.

## Web server settings

Set `NGINX_*` [environment variables](../../../apps/environment-variables.md) on the app service to change Nginx, such as
`NGINX_HEADERS_CONTENT_SECURITY_POLICY` or `NGINX_STATIC_EXPIRES`. Do not add an `nginx.conf` to the repository.
Changes apply with the next deployment.

## Development workspace

In a [development workspace](../../../apps/workspaces.md), the app service runs the Vite development server in a
Node.js image instead of Nginx. Expect these differences:

- Setup installs dependencies from the lockfile. Run setup again after you change dependencies.
- The server starts through Vite's API with your Vite configuration file, not with the `dev` script in `package.json`.
  Options in that script do not apply. `vite` must be a dependency of the project.
- The server listens on port 8080 and the container's health checks probe that port. Do not change the port.
- Vite rejects host names it does not know. Allow the environment's hosts in `server.allowedHosts` of your Vite
  configuration.
- To start the server another way, set `WORKSPACE_NODE_COMMAND` on the app service. The command must listen on
  `$HOST:$PORT` and poll for file changes itself.
