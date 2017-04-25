# Import existing WordPress website

There are different way to import existing WordPress website:

* [Via duplicator archive](#via-duplicator-archive) (recommended)
* [Via separate archives](#via-separate-archives)
* [Manual import](#manual)

## Via duplicator archive

Install <a href="https://wordpress.org/plugins/duplicator/" target="_blank">duplicator plugin</a> on your existing website. Go to admin part of your WordPress website and create a new package via duplicator.

Now navigate to `Apps > Deploy` and choose duplicator archive as data source on the 2nd step.

## Via separate archives

Alternatively, you can import WordPress via separate archives for code, database and files. We support `.zip`, `.gz`, `.tar.gz`, `.tgz` and `.tar` archives. 

> For big archives we recommend [importing it manually](#manual) after you deploy an app

## Manual

In case your WordPress website is huge it makes sense to import your database/files manually from the server. Follow these steps:
    
1. Deploy your WordPress website from a git repository without upload database and files
2. Once the app is deployed, go to `Stack > nginx-php` and copy SSH command
3. Connect the container by SSH and navigate to WordPress docroot (normally it's `/srv/app`)
4. Copy your database archive here using wget or scp, unpack the archive
5. Import unpacked database dump using `wp dm import my-db-dump.sql`
6. Now let's import your files, cd to `/srv/files`
7. Copy your files archive here using wget or scp and unpack the archive
8. That's it! Clear app cache from the dashboard and don't forget to remove archives and extracted db dump
