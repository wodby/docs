# Monitoring

## Single-server setup

Currently, Wodby does not provide monitoring tools for your servers or applications out of the box in a single-server setup. 

##### Servers monitoring

We recommend connecting your server manually to [NewRelic Servers](https://docs.newrelic.com/docs/servers) or [NewRelic Infrastructure](https://newrelic.com/infrastructure) (or other 3rd party monitoring tool of your choice) to track essentials metrics like CPU / RAM / Disk consumption. Nothing specific required during the installation, just follow the official guide.

##### Containers / Applications monitoring

Additionally, if you want to see resources consumption per container or per application, we recommend using  [`ctop`](https://github.com/bcicen/ctop). 

Installation:
```bash
sudo wget https://github.com/bcicen/ctop/releases/download/v0.6.1/ctop-0.6.1-linux-amd64 -O /usr/local/bin/ctop
sudo chmod +x /usr/local/bin/ctop
```

Show containers of a specific application instance:
```bash
ctop -f [INSTANCE UUID]
``` 

Press `S` to sort containers by CPU / RAM consumption. 
