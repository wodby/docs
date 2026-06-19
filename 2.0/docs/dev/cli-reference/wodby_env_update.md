# `wodby env update`

Update environment

```
wodby env update ID [flags]
```

### Options

```
      --data string    JSON request body
  -f, --file string    Path to JSON request body
  -h, --help           help for update
      --name string    Environment machine name
      --title string   Environment title
      --type string    Environment type: prod, staging, test, dev, or feature
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

* [wodby env](wodby_env.md)	 - Manage environments

