# Connect Drupal to Solr

The Wodby Drupal catalog stack supports SolrCloud with ZooKeeper. Both the `solr` and `zookeeper` stack services are
disabled by default, so enable both services and deploy them before configuring Drupal.

Solr creates a collection named `default` with its generic `_default` configset. Drupal's Search API Solr module must
replace that configset before the collection can index Drupal content.

## Install Search API Solr

Add the module to your Composer project and enable its administration module:

```bash
composer require drupal/search_api_solr
vendor/bin/drush en search_api_solr search_api_solr_admin -y
```

Deploy the updated code, then go to `Configuration > Search and metadata > Search API` in Drupal and add a server.

## Configure the server

Name the server `Solr` so its machine name is `solr`. Select the `Solr` backend and the `Solr Cloud with Basic Auth`
connector, then enter:

| Setting | Value |
| --- | --- |
| HTTP protocol | `http` |
| Solr node | `solr` |
| Solr port | `8983` |
| Solr path | `/` |
| Default Solr collection | `default` |
| Solr host context | `solr` |
| Username | `solr` |
| Password | Leave blank when the server machine name is `solr` |

The Drupal PHP service receives the internal Solr hostname and generated password through its stack link. Wodby's
generated `wodby.settings.php` applies the password to the Search API server whose machine name matches the linked Solr
service. It does not replace the connector's `Solr node` value, so enter `solr` explicitly.

`localhost` points back to the Drupal PHP container. A server saved with `localhost` cannot reach the separate Solr app
service.

## Upload the Drupal configset

After saving the server, an incompatible-schema warning is expected while the collection still uses `_default`.

1. Open the Search API server's detail page.
2. Select `Upload configset`.
3. Confirm that the configset may be uploaded or overwritten.
4. Use one shard.
5. Submit the upload.

The Search API Solr Admin module uploads a configuration generated for the installed module version and updates the
`default` collection. Create and configure a Search API index after the server and collection both report as available.

Upload the configset again whenever Search API Solr reports that the schema is outdated, then reindex the affected
indexes.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Server cannot be reached | `Solr node` is `solr`, not `localhost`; both Solr and ZooKeeper are enabled and deployed |
| Server is reachable but collection is unavailable | `Default Solr collection` is `default` |
| Authentication fails | Server machine name is `solr`, the generated Wodby settings file is included, and username is `solr` |
| Schema is incompatible | Upload or overwrite the configset from the Search API server page |

See the [Solr catalog guide](../solr/index.md) for collection and authentication behavior and the
[Search API Solr project](https://www.drupal.org/project/search_api_solr) for module releases and compatibility.
