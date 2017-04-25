# Importing Existing Drupal Website

There are different way to import existing Drupal website:

* [Via drush archive](#via-drush-archive) (recommended)
* [Via separate archives](#via-separate-archives)
* [Manual import](#manual)

## Via drush archive

First, make sure you have <a href="http://www.drush.org/en/master/install/" target="_blank">Drush installed</a>, go to your Drupal website docroot and execute a command:

```bash
$ drush archive-dump
```

or

```bash
$ drush ard
```

You should see output like:

```bash
$ drush ard
Archive saved to /Users/johndoe/drush-backups/archive-dump/20150604001227/drupalapp.20150604_001228.tar.gz
/Users/johndoe/drush-backups/archive-dump/20150604001227/drupalapp.20150604_001228.tar.gz
```

Now navigate to `Apps > Deploy` and choose drush archive on the 2nd step

## Via separate archives

Alternatively, you can import Drupal via separate archives for code, database and files. We support `.zip`, `.gz`, `.tar.gz`, `.tgz` and `.tar` archives. 

> For big archives we recommend [importing it manually](#manual) after you deploy an app

## Manual

In case your Drupal website is huge it makes sense to import your database/files manually from the server. Follow these steps:
    
1. Deploy your Drupal website from a git repository without upload database and files
2. Once the app is deployed, go to `Stack > nginx-php` and copy SSH command
3. Connect the container by SSH and navigate to Drupal docroot (normally it's `/srv/app`)
4. Copy your database archive here using wget or scp, unpack the archive
5. Import unpacked database dump using `drush sql-cli < my-db-dump.sql`
6. Now let's import your files, cd to `/srv/files`
7. Copy your files archive here using wget or scp and unpack the archive
8. That's it! Clear app cache from the dashboard and don't forget to remove archives and extracted db dump
