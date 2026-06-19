# `wodby completion zsh`

Generate the autocompletion script for zsh

### Synopsis

Generate the autocompletion script for the zsh shell.

If shell completion is not already enabled in your environment you will need
to enable it.  You can execute the following once:

	echo "autoload -U compinit; compinit" >> ~/.zshrc

To load completions in your current shell session:

	source <(wodby completion zsh)

To load completions for every new session, execute once:

#### Linux:

	wodby completion zsh > "${fpath[1]}/_wodby"

#### macOS:

	wodby completion zsh > $(brew --prefix)/share/zsh/site-functions/_wodby

You will need to start a new shell for this setup to take effect.


```
wodby completion zsh [flags]
```

### Options

```
  -h, --help              help for zsh
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

