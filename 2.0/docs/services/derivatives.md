# Derivative services

Derivative service is a service that derives most of its configuration from the main service (it's difference from [inheritance](template.md#from)). For example
`ssh` derivative service of
`php` will have all the environment variables and versions configured for PHP but will override certain parameters such as
`type`, `args`  and endpoints.

Derivative services defined under [`derivatives` section](template.md#derivatives) in a service template.
