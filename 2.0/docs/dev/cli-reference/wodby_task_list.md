# `wodby task list`

List tasks

```
wodby task list [flags]
```

### Options

```
      --app string        App ID
  -h, --help              help for list
      --instance string   App instance ID
      --org string        Organization ID
      --page int          Page number
      --page-size int     Page size
      --project string    Project ID or comma-separated project IDs
      --scope string      Task scope: project_and_org, org_only, or user_only
      --search string     Search query
      --statuses string   Comma-separated statuses
      --without-origin    Only tasks without origin
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

