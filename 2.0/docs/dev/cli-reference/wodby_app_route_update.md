# `wodby app route update`

Update app route

```
wodby app route update ID [flags]
```

### Options

```
      --action string              Route action: BACKEND or REDIRECT
      --data string                JSON request body
      --disabled                   Set disabled state
  -f, --file string                Path to JSON request body
  -h, --help                       help for update
      --main                       Set main route state
      --path string                Route path
      --path-type string           Route path type: PREFIX or EXACT
      --primary                    Set primary route state
      --redirect-host string       Redirect host
      --redirect-path string       Redirect path
      --redirect-scheme string     Redirect scheme
      --redirect-status-code int   Redirect status code
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

