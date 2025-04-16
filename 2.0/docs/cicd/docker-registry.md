# Docker Registry

CI/CD on Wodby that works via Wodby CLI will push built images in the
`wodby ci release` command to a docker registry associated with your application. By default, it's [Wodby Registry](wodby-registry.md), but optionally can be one of the registry integrations like [Docker Hub](../integrations/docker.md) or [Distribution](../integrations/distribution.md). 
