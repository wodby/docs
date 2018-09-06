You can profile your application via blackfire.io by following the next steps:

* Enable blackfire probe extension by adding the environment variable `PHP_BLACKFIRE=1` to PHP container
* Enable blackfire agent service in your stack
* Add environment variables `BLACKFIRE_SERVER_ID` and `BLACKFIRE_SERVER_TOKEN` to blackfire agent service with appropriate values from your blackfire.io profile
* Add environment variables `BLACKFIRE_CLIENT_ID` and `BLACKFIRE_CLIENT_TOKEN` to PHP service with appropriate values from your blackfire.io profile
* Install blackfire companion extension for [Chrome](https://blackfire.io/docs/integrations/chrome) or [Firefox](https://blackfire.io/docs/integrations/firefox)
* Start profiling your app via the extension and see data from blackfire.io dashboard

Fore more details please refer to the [blackfire official documentation](https://blackfire.io/docs/introduction)
