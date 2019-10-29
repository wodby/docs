This project uses [træfik](https://docs.traefik.io) to route traffic to different containers. Træfik is a modern HTTP reverse proxy and load balancer made to deploy microservices with ease. To understand the basics of Traefik it is suggested to check Træfik's documentation page: https://docs.traefik.io/

<img src="https://docs.traefik.io/assets/img/traefik-architecture.png" />

Image: Multi-domain set-up example
(Source: traefik.io)

There are two ways how you can run multiple projects:

### Single port

In this case you will run a stand-alone traefik that will be connected to docker networks of your projects:

1. Download `traefik.yml` file (part of `docker4x.tar.gz` archive). Place it separately from your projects, it will be a global traefik container that will route requests to your projects on a specified port 
2. Now we need to provide traefik names of docker networks of our projects. Let's say projects directories with `docker-compose.yml` named `foo` and `bar`. Docker Compose will create default docker networks for these projects called `foo_default` and `bar_default`. Update external networks names accordingly in `traefik.yml`
3. In `docker-compose.yml` of your projects comment out `traefik` service and make sure `traefik.http.*` labels have `${PROJECT_NAME}_` prefix
4. Make sure`$PROJECT_BASE_URL` and `$PROJECT_NAME` (in `.env` file) differ, both hosts point to `127.0.0.1` in `/etc/hosts`    
5. Run your projects: `make` (or `docker-compose up -d`) 
6. Run stand-alone traefik: `docker-compose -f traefik.yml up -d` 
7. Now when you visit URL from `$PROJECT_BASE_URL`, traefik will route traffic to the corresponding docker networks 

!!! warning "For macOS users with docker-sync"
    Make sure names of `syncs` in `docker-sync.yml` are unique per project. The recommended way is to run a stand-alone docker-sync with syncs definition for all projects. Do not forget to update `src` paths for projects 

### Different ports 

Alternatively, instead of running a stand-alone traefik, you can just run default traefik containers on different ports. Just a few things to make sure:

* Ports of `traefik` service in your `docker-compose.yml` files differ 
* `traefik.http.*` labels have `${PROJECT_NAME}_` prefix
* `$PROJECT_BASE_URL` and `$PROJECT_NAME` (in `.env` file) differ, both hosts point to `127.0.0.1` in `/etc/hosts`
