# `wodby task repeat`

Repeat task

```
wodby task repeat ID [flags]
```

### Options

```
      --data string        JSON request body
  -f, --file string        Path to JSON request body
      --force              Force repeat
  -h, --help               help for repeat
      --timeout duration   Maximum time to wait (default 10m0s)
      --wait               Wait for the created task or deployment to finish
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

* [wodby task](wodby_task.md)	 - Manage tasks

