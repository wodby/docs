# Continuous Integration and Delivery

You can use Wodby as a part of your CI/CD workflow for deploying environments on demand. We recommend using the following workflow for your CI/CD process:  

1. [Deploy your application via Wodby](../apps/deploy.md)
2. Use docker containers compatible with Wodby's bundles for your build. For Drupal and WordPress apps we recommend using <a href="https://github.com/wodby/docker4drupal" target="_blank">docker4drupal</a> and <a href="https://github.com/wodby/docker4wordpress" target="_blank">docker4wordpress</a>
3. Run tests
4. Upload the deployment tarball to an external storage like AWS Simple Safe Storage (S3)
5. Use [Wodby API](../api/README.md) to deploy a new instance of your app 
6. Deploy your tarball to the newly created instance

## CI/CD for Drupal 

### CircleCI example with Drupal 8

1. [Deploy](../apps/deploy.md) your Drupal 8 app via Wodby
2. Connect your repository to <a href="https://circleci.com/" target="_blank">CircleCI</a>
3. Copy the content of the `circleci` directory from this <a href="https://github.com/Wodby/wodby-ci/tree/master/circle-ci/scripts" target="_blank">this repository</a> to your D8 docroot. It contains the following files:
    * `scripts/composer.json`, contains information about Wodby PHP SDK for composer 
    * `scripts/wodby.php`, this script will deploy a new instance on Wodby with the tarball we get from the build 
    * `scripts/tests.sh`, this shell script will run 4 test suites from Drupal core (just for demo purposes) inside of the container 
    * `docker-compose.yml`, it's a simplified version of compose file from <a href="https://github.com/wodby/docker4drupal" target="_blank">docker4drupal</a>. These containers will be used to spin up the environment for your tests
    * `circle.yml`, in this file we tell CircleCI to spin our environment with docker containers, run our tests, prepare the deployment tarball and upload it AWS S3, run `wodby.php` file to deploy a new application instance and import the tarball
4. Our `scripts/tests.sh` file will run 4 random tests, we need to provide phpunit the information about our environment. Copy `core/phpunit.xml.dist` to `core/phpunit.xml` and adjust values of `SIMPLETEST_BASE_URL` to `http://nginx` and `SIMPLETEST_DB` to `mysql://drupal:drupal@mariadb/drupal`
5. We will use AWS S3 to store our tarballs. Create an S3 bucket. Generate access key for IAM user with permissions to upload to your AWS S3 bucket
6. Go to your CircleCI project settings page and navigate to _AWS Permissions_. Enter your AWS IAM key ID and access key
7. Now we need to set environment variables in CircleCI for our scripts. Navigate to _Environment Variables_ on the project settings page. Add the following environment variables:
    * `AWS_S3_BUCKET` - the name of AWS S3 bucket where we will upload deployment tarballs
    * `AWS_S3_FILE_NAME` - the name of the tarball file for this project
    * `WODBY_API_TOKEN` - copy the token from your Wodby profile page
    * `WODBY_ORG_ID` - open Wodby dashboard homepage and copy the UUID from the address url
    * `WODBY_SERVER_ID` - navigate to your server page from the Wodby dashboard and copy the UUID from the address url
    * `WODBY_APP_ID` - navigate to your application pages _Settings_ tab and copy the value of `Application UUID`
    * `WODBY_SOURCE_INSTANCE_ID` - from the same tab copy the value of `Instance UUID`. This instance will be used as the source of database and files for the newly deployed instance
8. That's it! Now commit and push all the files. CircleCI will automatically trigger the build process. 
     

### Jenkins

TBD