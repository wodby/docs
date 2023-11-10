# Variable integration

Variable is the simplest form of Wodby integration. Can be added to any non-external app service. When added it adds environment variables to the corresponding container with the values from the integration. 

For example, when you create a `Sentry` integration with a DSN value and then add it to an app service, the environment variable `$SENTRY_DSN=[value]` will be automatically added to the container with the specified value from the integration.

You can create your own variable providers from the _Providers_ tab.
