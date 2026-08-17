# CLI commands

Run infrastructure commands as root on the connected server. Infrastructure 7 configures `/root/.kube/config` during installation. If the default config is unavailable, add `--kubeconfig=/etc/kubernetes/admin.conf` to each `kubectl` command.

## Infrastructure 7

### Check cluster status

```shell
kubectl get nodes -o wide
kubectl get pods --all-namespaces -o wide
```

Wodby's system workloads run in the `wodby` namespace:

```shell
kubectl -n wodby get pods -o wide
```

### Restart Wodby Agent

```shell
kubectl -n wodby rollout restart deployment/agent
kubectl -n wodby rollout status deployment/agent --timeout=5m
```

### Restart Edge

Edge owns the server's public ports, so restarting it can cause a brief interruption:

```shell
kubectl -n wodby rollout restart deployment/edge
kubectl -n wodby rollout status deployment/edge --timeout=5m
```

### View system workload logs

```shell
kubectl -n wodby logs deployment/agent --since=30m --timestamps
kubectl -n wodby logs deployment/edge --since=30m --timestamps
kubectl -n wodby logs statefulset/etcd --since=30m --timestamps
```

### Restart host runtime services

Restarting these services interrupts applications on the server. Take a provider snapshot and verify that no maintenance operation is running first.

```shell
systemctl restart docker
systemctl restart cri-docker.socket kubelet
kubectl get nodes
kubectl get pods --all-namespaces
```

### Host service logs

```shell
journalctl -u kubelet -u docker -u cri-docker.service --since "30 minutes ago"
journalctl -u wodby-installer --since "30 minutes ago"
```

### Check installed component versions

```shell
cat /opt/wodby/etc/infrastructure-7.env
kubectl version
docker version
kubectl -n wodby get deployment agent edge -o custom-columns=NAME:.metadata.name,IMAGE:.spec.template.spec.containers[0].image
```

The Kubernetes deployment image is authoritative for Agent and Edge patch versions on a running server; the recorded installation profile describes what the installer originally applied.

### Clean up failed task Pods

Review the list before deleting anything:

```shell
kubectl get pods --all-namespaces | grep 'task-' | grep -E 'Error|Failed'
```

Delete a confirmed failed task Pod with:

```shell
kubectl -n INSTANCE_UUID delete pod POD_NAME
```

## Infrastructure 6 and older

The following commands are retained for existing legacy servers. Do not use the Infrastructure 7 systemd or kubeadm assumptions on these hosts.

### Restart Wodby Agent

```shell
docker rm -f $(docker ps | grep wodbycloud/agent | awk '{ print $1 }')
```

### Restart Edge

```shell
docker rm -f $(docker ps | grep wodby/edge-alpine | awk '{ print $1 }')
```

### Restart Docker and Kubernetes services

```shell
systemctl stop kube-apiserver
systemctl stop kube-controller
systemctl stop kube-kubelet
systemctl stop kube-proxy
systemctl stop kube-scheduler
systemctl stop docker

systemctl start docker
systemctl start kube-apiserver
systemctl start kube-controller
systemctl start kube-kubelet
systemctl start kube-proxy
systemctl start kube-scheduler
```

### Check node and namespaces

```shell
kubectl describe node 127.0.0.1
kubectl get namespaces
```

## General host checks

```shell
df -h
vmstat -Sm 1
journalctl -f
```
