# CLI commands

## Restart docker and kube services

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

## Check node status

```shell
kubectl describe node 127.0.0.1
```

## Check namespaces (deployed instances)

```shell
kubectl get ns
```

## System logs

```shell
journalctl -f
```

## Check disk space

```shell
df -h
ncdu /
```

## Check memory stats

```shell
vmstat -Sm 1
```