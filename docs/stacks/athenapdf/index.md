# AthenaPDF

AthenaPDF is an HTML to PDF converter and drop-in replacement for wkhtmltopdf

[Full documentation](https://github.com/arachnys/athenapdf/tree/master/weaver)

## Usage 

via Wodby, port `80`:

```shell
curl http://athenapdf/convert\?auth\=wodby-athenapdf\&url\=http://google.com/ |> out.pdf
```

For local environment (port `8080`):

```shell
curl http://athenapdf:8080/convert\?auth\=wodby-athenapdf\&url\=http://google.com/ |> out.pdf
```

## Environment variables 

| Environment Variable          | Default Value     | Description |
| ----------------------------- | ----------------- | ----------- |
| `WEAVER_AUTH_KEY`             | `wodby-athenapdf` |             |
| `WEAVER_ATHENA_CMD`           | `athenapdf -S`    |             |
| `WEAVER_MAX_WORKERS`          | `10`              |             |
| `WEAVER_MAX_CONVERSION_QUEUE` | `50`              |             |
| `WEAVER_WORKER_TIMEOUT`       | `90`              |             |
| `WEAVER_CONVERSION_FALLBACK`  | `false`           |             |

## Changelog

### 1.0.3

* Default [memory request](../config.md#resources) set to 16m

### 1.0.2

* Version freeze to 2.10.0

### 1.0.1

* AthenaPDF now has public port with technical domain by default

### 1.0.0

Initial release