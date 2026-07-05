# Wodby SDKs

Wodby publishes generated SDKs for API automation. The SDKs use API key authentication: send the key as `X-API-KEY`.

Use the [2.0 API reference](https://wodby.com/docs/2.0/api/) for the current public `/v1` REST API. Use SDK repository documentation for language-specific generated class and method names.

## Compatibility

The SDKs listed below target the current Wodby 2.0 public `/v1` API and are generated from the OpenAPI schema published in the [API reference](https://wodby.com/docs/2.0/api/).

SDK package versions `4.0.0` and newer target the Wodby 2 API `/v1`. If you maintain an older integration that uses the previous v3 SDK surface, keep it pinned to a compatible `3.x` package version until you migrate.

## Official SDKs

| Language | Package | Registry | Repository | Generated docs |
| --- | --- | --- | --- | --- |
| PHP | `wodby/wodby-sdk-php` | [Packagist](https://packagist.org/packages/wodby/wodby-sdk-php) | [wodby/wodby-sdk-php](https://github.com/wodby/wodby-sdk-php/tree/2.0) | [SwaggerClient-php/docs](https://github.com/wodby/wodby-sdk-php/tree/2.0/SwaggerClient-php/docs) |
| Python | `wodby` | [PyPI](https://pypi.org/project/wodby/) | [wodby/wodby-sdk-python](https://github.com/wodby/wodby-sdk-python/tree/2.0) | [src/docs](https://github.com/wodby/wodby-sdk-python/tree/2.0/src/docs) |
| JavaScript and TypeScript | `@wodby/sdk` | [npm](https://www.npmjs.com/package/@wodby/sdk) | [wodby/wodby-sdk-js](https://github.com/wodby/wodby-sdk-js/tree/2.0) | [src](https://github.com/wodby/wodby-sdk-js/tree/2.0/src) |
| Go | `github.com/wodby/wodby-sdk-go/v4/pkg` | [pkg.go.dev](https://pkg.go.dev/github.com/wodby/wodby-sdk-go/v4/pkg) | [wodby/wodby-sdk-go](https://github.com/wodby/wodby-sdk-go/tree/2.0) | [pkg/docs](https://github.com/wodby/wodby-sdk-go/tree/2.0/pkg/docs) |

## Install

PHP:

```bash
composer require wodby/wodby-sdk-php
```

Python:

```bash
pip install wodby
```

JavaScript and TypeScript:

```bash
npm install @wodby/sdk
```

Go:

```bash
go get github.com/wodby/wodby-sdk-go/v4/pkg
```

## Authentication

Set `WODBY_API_KEY` in your shell or CI secrets, then pass it to the SDK configuration as the `X-API-KEY` API key.

Python example:

```python
import os
import wodby

configuration = wodby.Configuration()
configuration.api_key["X-API-KEY"] = os.environ["WODBY_API_KEY"]
```

JavaScript example:

```js
const { Configuration, OrgsApi } = require('@wodby/sdk');

const api = new OrgsApi(new Configuration({
  basePath: 'https://api.wodby.com/v1',
  apiKey: process.env.WODBY_API_KEY,
}));
```

PHP example:

```php
<?php

require_once './vendor/autoload.php';

$config = \Wodby\Api\Configuration::getDefaultConfiguration()
    ->setApiKey('X-API-KEY', getenv('WODBY_API_KEY'));
```

## Choosing between API, SDKs, and CLI

- Use the 2.0 REST API directly for simple scripts, debugging, and unsupported languages.
- Generate a client from the 2.0 OpenAPI schema when you want typed models for new `/v1` integrations.
- Use the official SDK packages when you want generated models and request helpers in a supported language.
- Use [Wodby MCP](mcp.md) when an AI assistant needs Wodby context or deployment diagnostics.
- Use the [Wodby CLI](cli.md) for CI build, release, and deploy workflows.

## Related pages

- [Wodby API](api.md)
- [Wodby MCP](mcp.md)
- [API keys](api-keys.md)
- [Wodby CLI](cli.md)
