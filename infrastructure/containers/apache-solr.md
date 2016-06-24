# Apache Solr 

> Service: Search engine

* [Access](#access)
    * [Solr admin panel](#solr-admin-panel)
* [Logs](#logs)
* [Cores](#cores)
* [Configuration files](#configuration-files)
* [Integration with Drupal](#integration-with-drupal)
    * [Configuration files](#configuration-files)
    * [Connecting server](#connecting-server)

## Access

This container doesn't expose public ports. If you want to access the container itself please refer [to this article](access.md) (with no SSH).

### Solr admin panel

URL: You can find URL on `Instance > Containers > Solr` page<br>
Login: `admin` <br>

You can find password by connecting to the [nginx-php container](nginx-php/README.md) by SSH and executing: 
```bash
$ echo $WODBY_SOLR_PASSWORD`
```

## Logs

Logs can be found under `/var/log/`.

## Cores

By default Apache solr has one core called `wodby`.

## Configuration files

Solr configs located in a solr core directory under `/opt/solr/server/solr/cores/`. 

## Integration with Drupal

### Configuration files

For Drupal 7 and 8 Wodby automatically puts the following configuration files from <a href="https://www.drupal.org/project/search_api_solr" target="_blank">Search API Solr Search module</a> to the [default core](#cores) directory:

```
elevate.xml                
mapping-ISOLatin1Accent.txt
protwords.txt              
schema_extra_fields.xml    
schema_extra_types.xml     
schema.xml                 
solrconfig_extra.xml       
solrconfig.xml             
solrcore.properties        
stopwords.txt              
synonyms.txt
```

### Connecting server

1. Download and install <a href="https://www.drupal.org/project/search_api_solr" target="_blank">Search API Solr Search</a> module
2. Connect to [nginx-php container](nginx-php/README.md) by SSH
3. Execute the following commands to learn Solr basic auth password: 
```bash
$ echo $WODBY_SOLR_PASSWORD
``` 
4. Go to `Configuration » Search and metadata » Search API` and select Service class to "Solr service"  
5. In expanded settings fieldset specify:
```
HTTP protocol: http
Solr host: <Copy hostname from "Instance > Containers > Solr" page>
Solr port: 8983
Solr path: /solr/wodby
Basic authentication:
  Username: admin
  Password: <Put there password you acquired on step 3>
```

