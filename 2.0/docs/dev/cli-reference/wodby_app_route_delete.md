# `wodby app route delete`

Delete app route

```
wodby app route delete ID [flags]
```

### Options

```
  -h, --help               help for delete
      --timeout duration   Maximum time to wait (default 10m0s)
      --wait               Wait for the created task or deployment to finish
  -y, --yes                Confirm without prompting
```

### Options inherited from parent commands

```
      --access-token string     Access token
      --api-base-url string     Public REST API base URL (default "https://api.wodby.com/v1")
      --api-endpoint string     GraphQL API endpoint used by CI commands (default "https://apiv2.wodby.com/query")
      --api-key string          API key
      --ci-config-path string   Path to CI config (default "/tmp/.wodby-ci.json")
  -o, --output string           Output format: table or json (default "table")
      --verbose                 Verbose output
```

### SEE ALSO

* [wodby app route](wodby_app_route.md)	 - Manage app routes

