# `wodby completion fish`

Generate the autocompletion script for fish

### Synopsis

Generate the autocompletion script for the fish shell.

To load completions in your current shell session:

	wodby completion fish | source

To load completions for every new session, execute once:

	wodby completion fish > ~/.config/fish/completions/wodby.fish

You will need to start a new shell for this setup to take effect.


```
wodby completion fish [flags]
```

### Options

```
  -h, --help              help for fish
      --no-descriptions   disable completion descriptions
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

* [wodby completion](wodby_completion.md)	 - Generate the autocompletion script for the specified shell

