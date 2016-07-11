# CLI commands

The commands must be executed on the host machine (connected server) as a root.

## Docker 

Show currently running containers:
 
```bash
$ docker ps
```

Show running containers filtered by instance (namespace). You can find <INSTANCE_NAMESPACE> on the `[Instance] > Settings > Info` tab. 

```bash
$ docker ps | grep <INSTANCE_NAMESPACE>
```

Show running containers filtered by app. You can find <APP_UUID> on the `[Instance] > Settings > Info` tab.

```bash
$ docker ps | grep <APP_UUID>
```

List container images:

```bash
$ docker images
```

Connect to the container:

```bash
$ docker exec -ti <CONTAINER_ID> sh
```

You can find the full list of the CLI commands in <a href="https://docs.docker.com/engine/reference/commandline/cli/" target="_blank">the official documentation</a>

### Kubernetes

Kubectl located in `/opt/kubernetes/bin/kubectl`. Please refer to <a href="http://kubernetes.io/docs/user-guide/kubectl/kubectl/" target="_blank">the official documentation</a> for commands reference.

We strongly recommend to avoid modifying Kubernetes entities.