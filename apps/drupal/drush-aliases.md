# Drush aliases

Wodby provides integration with Drush for Drupal apps. Navigate `App page > Settings > Drush` and download the aliases file. 

Download and copy drush aliases into `~/.drush` or your local drush aliases directory. To use them navigate into your project repository directory and run (replace [tokens] with the real values):

```
$  drush @[org_name].[app_hostname].[instance_name] [drush_command]
```