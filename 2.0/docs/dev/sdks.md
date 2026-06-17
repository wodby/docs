# Wodby SDKs

Wodby publishes generated SDKs for API automation. The SDKs use API key authentication: send the key as `X-API-KEY`.

Use the [2.0 API reference](https://wodby.com/docs/2.0/api/) for the current public `/v1` REST API. Use SDK repository documentation for language-specific generated class and method names.

## Compatibility

The current 2.0 API reference documents the public `/v1` API contract.

The SDK repositories listed below are generated clients for the older v3 API surface. Use them for existing v3 SDK integrations. For new integrations against the 2.0 `/v1` API, use the OpenAPI schema from the [API reference](https://wodby.com/docs/2.0/api/) to generate a client or call the REST API directly.

## Official SDKs

| Language | Package | Repository | Generated docs |
| --- | --- | --- | --- |
| PHP | `wodby/wodby-sdk-php` | [wodby/wodby-sdk-php](https://github.com/wodby/wodby-sdk-php) | [SwaggerClient-php](https://github.com/wodby/wodby-sdk-php/tree/master/SwaggerClient-php) |
| Go | Go package in repository | [wodby/wodby-sdk-go](https://github.com/wodby/wodby-sdk-go) | [pkg](https://github.com/wodby/wodby-sdk-go/tree/master/pkg) |
| Python | `wodby` | [wodby/wodby-sdk-python](https://github.com/wodby/wodby-sdk-python) | [src](https://github.com/wodby/wodby-sdk-python/tree/master/src) |

## Install

PHP:

```bash
composer require wodby/wodby-sdk-php
```

Python:

```bash
pip install wodby
```

For Go, follow the generated package documentation in the [wodby-sdk-go](https://github.com/wodby/wodby-sdk-go) repository.

## Authentication

Set `WODBY_API_KEY` in your shell or CI secrets, then pass it to the SDK configuration as the `X-API-KEY` API key.

Python example:

```python
import os
import wodby

configuration = wodby.Configuration()
configuration.api_key["X-API-KEY"] = os.environ["WODBY_API_KEY"]

org_api = wodby.OrganizationApi(wodby.ApiClient(configuration))
orgs = org_api.get_orgs()
```

PHP example:

```php
<?php

require_once './vendor/autoload.php';

$config = \Wodby\Api\Configuration::getDefaultConfiguration()
    ->setApiKey('X-API-KEY', getenv('WODBY_API_KEY'));

$appApi = new \Wodby\Api\Client\ApplicationApi(new GuzzleHttp\Client(), $config);
$apps = $appApi->getApps();
```

## Choosing between API, SDKs, and CLI

- Use the 2.0 REST API directly for simple scripts, debugging, and unsupported languages.
- Generate a client from the 2.0 OpenAPI schema when you want typed models for new `/v1` integrations.
- Use the existing SDKs for integrations that already target the older v3 API surface.
- Use the [Wodby CLI](cli.md) for CI build, release, and deploy workflows.

## Related pages

- [Wodby API](api.md)
- [API keys](api-keys.md)
- [Wodby CLI](cli.md)
