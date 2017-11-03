# Monitoring

Currently, Wodby does not provide monitoring tools for your servers and applications in single-server setup. We recommend to connect your server manually to NewRelic Servers. Nothing specific required during the installation, just follow the official guide.

Additionally, if you want to see resources consumption per container or per application, we recommend installing  [`ctop`](https://github.com/bcicen/ctop):

```bash
sudo wget https://github.com/bcicen/ctop/releases/download/v0.6.1/ctop-0.6.1-linux-amd64 -O /usr/local/bin/ctop
sudo chmod +x /usr/local/bin/ctop
```

Show containers of a specific application instance:

```bash
ctop -f [INSTANCE UUID]
``` 

Press `S` to sort containers by CPU / RAM consumption. 
