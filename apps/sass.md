# Compile Sass

**Available only for bundle versions starting [3.2.0](../infrastructure/bundles/README.md)**

All Drupal and WordPress bundles contain <a href="https://github.com/wellington/wellington" target="_blank">wellington</a> - a light-weight  (unlike compass) go extension to LibSass.

You can configure auto-compilation of your Sass files via [post-deployment scripts](../deployment/post-deployment-scripts.md):
 
```yml
pipeline:
  - name: sass
    type: command
    command: /opt/wodby/bin/wt -b <output-css-dir> compile <input-sass-dir>
    directory: $WODBY_APP_DOCROOT
```