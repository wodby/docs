# Derivative services

Derivative service is a service that derives most of its configuration from the main service. For example `ssh` derivative service of `php` will have all the environment variables and versions configured for PHP but will override certain parameters such as `type`, `args`  and endpoints.
