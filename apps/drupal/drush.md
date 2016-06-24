# Drush 

The backend service of Drupal includes drush. 

## Access database

You can connect the database by executing the following command in the Drupal docroot inside of the [nginx-php container](nginx-php/README.md):

```bash
$ drush sql-cli
```
 
## Drush aliases 

Wodby provides integration with Drush for Drupal apps. Navigate `Instance page > Settings > Drush` and download the aliases file. 

Download and copy drush aliases into `~/.drush` or your local drush aliases directory. To use them navigate into your project repository directory and run (replace [tokens] with the real values):

```
$  drush @[org_name].[app_hostname].[instance_name] [drush_command]
```