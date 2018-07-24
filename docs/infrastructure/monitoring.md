# Monitoring

## Single-server infrastructure monitoring

As of infrastructure 5.x Wodby does not provide monitoring tools for your servers, we recommend connecting your server manually to [NewRelic Servers](https://docs.newrelic.com/docs/servers) or [NewRelic Infrastructure](https://newrelic.com/infrastructure) (or other 3rd party monitoring tool of your choice) to track essentials metrics like CPU / RAM / Disk consumption. Nothing specific required during the installation, just follow the official guide.

## Containers monitoring

Additionally, if you want to see resources consumption per container or per application, we recommend using  [`ctop`](https://github.com/bcicen/ctop). 

Installation:
```shell
sudo wget https://github.com/bcicen/ctop/releases/download/v0.6.1/ctop-0.6.1-linux-amd64 -O /usr/local/bin/ctop
sudo chmod +x /usr/local/bin/ctop
```

Show containers of a specific application instance:
```shell
ctop -f [INSTANCE UUID]
``` 

Press `s` to sort containers by CPU / RAM consumption. 

You can identify which application a container belongs by copying a container ID (CID column) and executing:

```shell
docker exec [CONTAINER_ID] sh -c 'echo $WODBY_APP_NAME'
```