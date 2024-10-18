# Service links

Service link is the representation of a service integration or communication with another service. The simplest example would be Nginx's service link to upstream/backend (e.g. PHP-FPM). Some links are mandatory, some are optional. If a link is mandatory, a stack where such service added must specify which service from the stack should be used for a link. For example, in Drupal stack the PHP service requires _Database_ link, you can set it to use container-based _MariaDB_ or an external _Cloud MySQL_.
