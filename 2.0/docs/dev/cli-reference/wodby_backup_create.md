# `wodby backup create`

Create backup

```
wodby backup create [flags]
```

### Options

```
      --bucket string          Storage bucket
      --data string            JSON request body
      --database-db string     Database DB ID
  -f, --file string            Path to JSON request body
  -h, --help                   help for create
      --integration int        Storage integration ID
      --name string            Backup name
      --service string         App service ID
      --storage-class string   Storage class
      --timeout duration       Maximum time to wait (default 10m0s)
      --wait                   Wait for the created task or deployment to finish
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

* [wodby backup](wodby_backup.md)	 - Manage backups

