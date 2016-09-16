# Drupal Multi-site

You can deploy your existing multi-site Drupal (only 7.x and 8.x) as separate apps (one per each site). Go to `Apps > Deploy` and follow these steps: 

* 1st step: Choose the git repository with the shared codebase 
* 2nd step: Choose source option `Use code from the selected git repo` and specify Multi-site directory (e.g. if you have a directory `sites/my-drupal-site` just specify `my-drupal-site`). This directory will be used to locate <a href="settings.html#settingsphp">`settings.php`</a> file in this directory. Also, <a href="settings.html#sitesphp">`sites.php`</a> file will be created automatically with mapping of all [domains attached via Wodby](../domains.md) to this sites directory.   
