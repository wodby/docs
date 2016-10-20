# Deployment via composer

## Drupal example

For drupal we recommend using <a href="https://github.com/drupal-composer/drupal-project" target+"_blank">drupal-composer</a> template. 

1. Add the following _wodby.yml_ to your repository:

```
pipeline:
  - name: Install dependencies
    type: command
    command: composer install
    directory: $WODBY_APP_ROOT
  - name: Add Wodby include to settings.php file
    type: command
    command: echo -e "isset(\$_SERVER['WODBY_CONF']) && include \$_SERVER['WODBY_CONF'] . '/wodby.settings.php';" >> settings.php
    only_if: "[ $(grep -ic wodby.settings.php settings.php) -eq 0 ]"
    directory: $WODBY_APP_DOCROOT/sites/$WODBY_APP_SUBSITE
  - name: Install Drupal if not installed
    type: command
    command: drush site-install -y
    only_if: "[ $(drush sqlq \"SHOW TABLES LIKE 'users'\" | grep -ic users) -eq 0 ]"
    directory: $WODBY_APP_DOCROOT/sites/$WODBY_APP_SUBSITE
```

2. Specify directory to the docroot (by default `web`) on the second step of application deployment form under advanced settings.