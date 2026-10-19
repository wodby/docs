# Google Analytics

Google Analytics is available in Wodby as a `variable` provider. Use it to inject a Google Analytics 4 web data stream
measurement ID into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| Measurement ID | Yes | `GOOGLE_ANALYTICS_MEASUREMENT_ID` |

The measurement ID must start with `G-` and contain uppercase letters or numbers after the prefix.

## Usage

After you create a Google Analytics integration and attach it to an app service or stack, Wodby injects
`GOOGLE_ANALYTICS_MEASUREMENT_ID` into the container.
