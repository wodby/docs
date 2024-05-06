# Valkey stack documentation

Valkey can be configured with the following [environment variables](https://github.com/wodby/valkey#environment-variables)

## Connecting to valkey

If you want to access valkey from the same server you can access it as:

```
redis://default:[valkey-pass]@[app-instance-uuid].valkey:6379
```

If you're accessing valkey externally you should expose valkey port dynamically via node and connect as following:

```
redis://default:[valkey-pass]@[node-ip]:[dynamic-node-valkey-port]
```

## Changelog

This changelog is for Valkey stack on Wodby, to see image changes see tags description on [repository page](https://github.com/wodby/valkey/releases).

### 0.1.0 

⬆️ Initial Valkey release 7.2.5
