# HTML stack documentation

## Deployment

### CI/CD

!!! info "CI/CD tutorial"
    For a detailed instructions of setting up CI/CD workflow see the main [deployment article](/apps/deploy.md#cicd)

The following services are CI services that will be built by default:

* HTTP server: `nginx` or `apache`

## Containers

### Nginx

{!stacks/_includes/containers/nginx.md!}

### Apache

{!stacks/_includes/containers/apache.md!}

## Changelog

This changelog is for HTML stack on Wodby, to see images changes see tags description on repository page: [nginx](https://github.com/wodby/nginx/releases) and [Apache](https://github.com/wodby/apache/releases).

### 0.1.0

Initial release
