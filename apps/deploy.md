# Deploying New Application with Wodby

Deployment of the new applications consist of 2 simple steps:

## Step 1: Choose Server and Bundle

Select one of the [**connected servers**](../servers/README.md) where you want to deploy your app. 
 
Choose a [**bundle**](../bundles/README.md) for deployment. 

Additionally, check optional services for deployment such as a cache storage, and search engine. Some services, such as backend, have different container implementations (Nginx + PHP 5.6 or Nginx + PHP7).
 
## Step 2: Enter App Name and Specify Data Sources

Enter the name of your application. The URL for your application will be automatically generated based on this name, you can optionally adjust it.

Specify data (codebase/database/files) sources for your application. Select one of the [**connected git repositories**](../git/README.md) or use Demo git server. Then choose one of the following options indicating how you want to import the data for your application. 

#### Use code from the selected git repo

> The option is not available for Demo wodby git server. 

This option indicates that your code will be used from the cloned git repository. Additionally, you can upload archives for database and files.

#### Use pre-configured preset

Wodby provides pre-configured presets (for [Drupal](drupal/preset.md) and [WordPress](wordpress/preset.md)). Existing files in the default branch will be removed. Files of the preset will be added. **The code won't be committed to your repository.** You will be able to see new files from the [remote workspace](remote-workspace/README.md) tab.

#### Import from separate archives

Upload three separate archives for code, database and files. The following formats are supported: `.zip .gz .tar.gz .tgz .tar`. Existing files in the default branch will be removed. Files from the extracted code/files archives will be added. **The code won't be committed to your repository.** You will be able to see new files from the [remote workspace](remote-workspace/README.md) tab. 

#### Application specific import

See details: 
* <a href="drupal/import.html#via-drush-archive">Import existing Drupal websites via drush archive</a> 
* <a href="wordpress/import.html#via-duplicator-archive">Import existing WordPress websites via duplicator archive</a> 
