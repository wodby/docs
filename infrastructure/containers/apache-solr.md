# Apache Solr 

Official website: <a href="http://lucene.apache.org/solr/" target="_blank">http://lucene.apache.org/solr/</a>

> Service: Search engine

* [Access](#access)
    * [Solr admin panel](#solr-admin-panel)
* [Version](#version)    
* [Logs](#logs)
* [Cores](#cores)
* [Configuration files](#configuration-files)
* [Integration with Drupal](#integration-with-drupal)
    * [Configuration files](#configuration-files)
    * [Connecting server](#connect)

## Access

This container doesn't provide SSH access, if you want to access the container please refer [to this article](access.md) (with no SSH).

### Solr admin panel

URL: You can find URL and login/password on `[Instance] > Bundle > Search engine` page.

## Version

The current version of Apache Solr can be found on `[Instance] > Bundle > Search engine` page.

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
2. Go to `Configuration » Search and metadata » Search API` and select Service class to "Solr service"  
3. In expanded settings fieldset specify:
```
HTTP protocol: http
Solr host: <Copy Internal hostname from "[Instance] > Bundle > Search engine">
Solr port: 8983
Solr path: /solr/wodby
Basic authentication:
  Username: admin
  Password: <Copy password from "[Instance] > Bundle > Search engine">
```

