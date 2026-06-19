# `wodby route create`

Create app route

```
wodby route create [flags]
```

### Options

```
      --action string      Route action: BACKEND or REDIRECT
      --data string        JSON request body
  -f, --file string        Path to JSON request body
  -h, --help               help for create
      --host string        Route host
      --letsencrypt        Request Let's Encrypt certificate
      --main               Make route the app instance main route
      --path string        Route path
      --path-type string   Route path type: PREFIX or EXACT
      --port int           Service port
      --primary            Make route primary for the service endpoint
      --service string     App service ID
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

* [wodby route](wodby_route.md)	 - Manage app routes

