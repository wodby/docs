# Service template

## Service types

| Type             | Description                                                        |
| -----------      | ------------------------------------------                         |
| `service`        | Stateless service, e.g. PHP-FPM                                    |
| `db`             | Database services, usually stateful sets                           |
| `config`         |                                                                    |
| `infrastructure` | Used for infrastructure apps, e.g. ingress, certmanager            |
| `nfs`            | Programmatically created NFS service, used only for shared storage |
| `ssh`            | Stateless service that can work with SSH keys                      |
| `cache`          | Cache storage, e.g. memcached                                      |
| `proxy`          | Proxy servers, reverse proxy servers, e.g. varnish                 |
 