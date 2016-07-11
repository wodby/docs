# Deploy new application via Wodby

Deployment of the new applications consist of 3 steps:

* [Step 1: Select a server](#step-1-select-a-server)
* [Step 2: Choose a bundle](#step-2-choose-a-bundle)
* [Step 3: Choose data source](#step-3-choose-data-source)
    * [Use code from the selected git repo](#use-code-from-the-selected-git-repo)
    * [Use pre-configured preset by Wodby](#use-pre-configured-preset)
    * [Import from separate archives](#import-from-separate-archives)
    * [Application specific import](#application-specific-import)

## Step 1: Select a server

Select one of the [connected servers](../servers/connecting-server/README.md) for deployment. The [infrastructure](../infrastructure/README.md) for the application will be deployed to this server.
 
## Step 2: Choose a bundle

Choose a [**bundle**](../infrastructure/bundles/README.md) for deployment. 

Additionally, check optional containers for deployment such as a cache storage, database management, search engine and reverse caching proxy. Some containers, such as [Nginx + PHP container](../infrastructure/containers/nginx-php/README.md), can be switched: using PHP 5.6 or PHP 7.
 
## Step 3: Specify Data Sources

Choose one of the [connected git repositories](../git/connecting-git/README.md) or use Demo git server. Then choose one of the following options indicating how you want to import the data (code/database/files) for your application. 

### Use code from the selected git repo

> The option is not available for Demo wodby git server. 

This option indicates that your code will be used from the cloned git repository. Additionally, you can upload archives for database and files.

### Use pre-configured preset

Wodby provides pre-configured presets (for [Drupal](drupal/preset.md) and [WordPress](wordpress/preset.md)). Existing files in the default branch will be removed. Files of the preset will be added. **The code won't be committed to your repository.** You will be able to see new files from the [remote workspace](remote-workspace/README.md) tab.

### Import from separate archives

Upload three separate archives for code, database and files. The following formats are supported: `.zip .gz .tar.gz .tgz .tar`. Existing files in the default branch will be removed. Files from the extracted code/files archives will be added. **The code won't be committed to your repository.** You will be able to see new files from the [remote workspace](remote-workspace/README.md) tab. 

### Application specific import

See details: 
* <a href="drupal/import.html#via-drush-archive">Import existing Drupal websites via drush archive</a> 
* <a href="wordpress/import.html#via-duplicator-archive">Import existing WordPress websites via duplicator archive</a> 
