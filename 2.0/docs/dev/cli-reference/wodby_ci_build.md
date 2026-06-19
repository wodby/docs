# `wodby ci build`

Build images

```
wodby ci build [OPTIONS] [SERVICE]... [flags]
```

### Options

```
      --build-arg stringArray       Additional build argument in the 'NAME=VALUE' format. Repeatable
      --build-arg-env stringArray   Environment variable name to forward as a docker build argument. Repeatable
      --cache-backend string        Build cache backend: auto, local, registry, none (default "auto")
      --cache-dir string            Build cache directory for local backend
      --cache-from stringArray      Additional buildx cache source. Repeatable
      --cache-mode string           Build cache export mode (default "max")
      --cache-ref string            Build cache reference for registry backend
      --cache-to stringArray        Additional buildx cache destination. Repeatable
  -f, --dockerfile string           Relative path to dockerfile
      --from string                 Relative path to codebase (default ".")
  -h, --help                        help for build
      --to string                   Codebase destination path in container (default ".")
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

