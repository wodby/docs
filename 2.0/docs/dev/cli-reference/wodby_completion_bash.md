# `wodby completion bash`

Generate the autocompletion script for bash

### Synopsis

Generate the autocompletion script for the bash shell.

This script depends on the 'bash-completion' package.
If it is not installed already, you can install it via your OS's package manager.

To load completions in your current shell session:

	source <(wodby completion bash)

To load completions for every new session, execute once:

#### Linux:

	wodby completion bash > /etc/bash_completion.d/wodby

#### macOS:

	wodby completion bash > $(brew --prefix)/etc/bash_completion.d/wodby

You will need to start a new shell for this setup to take effect.


```
wodby completion bash
```

### Options

```
  -h, --help              help for bash
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

