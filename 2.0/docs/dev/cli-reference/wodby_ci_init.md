# `wodby ci init`

Initialize config for CI process

```
wodby ci init [OPTIONS] WODBY_APP_SERVICE_ID|WODBY_BUILD_ID [flags]
```

### Options

```
  -i, --build-id string   Custom build id (used if can't identify automatically)
  -n, --build-num int     Custom build number (used if can't identify automatically)
  -c, --context string    Build context (default: current directory)
      --dind              Use data container for sharing files between commands
      --fix-permissions   Fix codebase permissions explicitly. WARNING: this can change ownership of files in the project directory
  -h, --help              help for init
  -p, --provider string   Override detected build provider name
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

