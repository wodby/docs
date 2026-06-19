# `wodby ci release`

Push images

```
wodby ci release [SERVICE...] [flags]
```

### Options

```
  -b, --branch-tag             Additionally push tag with the current git branch name
  -h, --help                   help for release
  -l, --latest-branch string   Update latest tag when built from this branch (default "master")
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

