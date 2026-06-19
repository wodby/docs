# `wodby ci run`

Run container

```
wodby ci run [OPTIONS] -s SERVICE | -i IMAGE [flags]
```

### Options

```
      --entrypoint string   Entrypoint
  -e, --env strings         Environment variables
      --env-file string     Env file
  -h, --help                help for run
  -i, --image string        Image
  -p, --path string         Working dir (relative path)
  -s, --service string      Service
  -u, --user string         User (defaults to current uid:gid for bind-mounted contexts, except 1000:1000)
  -v, --volume strings      Volumes
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-endpoint string     GraphQL API endpoint used by CI commands (default "https://apiv2.wodby.com/query")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby ci](wodby_ci.md)	 - ci commands

