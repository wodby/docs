# Monitoring

Wodby reports server reachability and task results, but it does not provide a
complete host-monitoring and alerting service. Install a monitoring agent from
your cloud provider or a service such as New Relic Infrastructure, Datadog, or
your existing observability platform.

At minimum, monitor:

- CPU utilization and load average;
- available memory and out-of-memory events;
- filesystem bytes and inodes;
- disk latency and throughput;
- network availability and latency;
- Docker, containerd, kubelet, and Kubernetes control-plane health; and
- restarts and readiness of application and Wodby system workloads.

Alert before the server exhausts disk or memory rather than relying only on a
Wodby task failure.

## Infrastructure 7

Use Kubernetes to inspect node and workload state:

```shell
kubectl get nodes -o wide
kubectl get pods --all-namespaces -o wide
kubectl -n wodby get pods -o wide
```

For one application instance:

```shell
kubectl get pods -n INSTANCE_UUID -o wide
kubectl describe pod -n INSTANCE_UUID POD_NAME
```

If your monitoring setup provides the Kubernetes Metrics API, current resource
usage is available through:

```shell
kubectl top node
kubectl top pods -n INSTANCE_UUID --containers
```

`kubectl top` is not a historical monitoring system and will fail when no
Metrics API provider is installed. Use your monitoring platform for retention,
dashboards, and alerts.

Host-level snapshots remain useful during an incident:

```shell
free -h
df -hT
vmstat 1
docker stats --no-stream
```

See [CLI commands](cli.md#infrastructure-7) for system workload logs and
component checks.

## Infrastructure 6 and older

Legacy single-server installations expose application containers directly
through Docker. `docker stats` provides a live resource snapshot. If you choose
to install a third-party terminal tool such as
[`ctop`](https://github.com/bcicen/ctop), follow its current release and checksum
instructions instead of using an old pinned binary from these docs.

These tools show current container usage only. Continue to use a host-monitoring
agent for history and alerts, and do not apply Infrastructure 7 kubeadm or
namespace assumptions to a legacy server.
