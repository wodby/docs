# Memory consumption of Wodby infrastructure

The table below demonstrates how much memory our infrastructure consumes with the different # of apps. 

Test conditions:

* The test was performed on `AWS EC2 t2.micro (1 CPU 1GB RAM)`
* OS was Linux Debian 8
* Deployments of `new Drupal 7 (D7)` apps were tested, which included 3 containers: nginx + php-fpm, mariadb, redis
* There was no traffic on deployed apps
* The date of the test is `14.04.16`
* Memory consumption results were taken with `free -h`

> The results may vary depending on [the infrastructure version](versioning.md). 

| Total | Used before connecting to Wodby | After connection | After deploying 1st D7 app | After 2nd D7 app | After 3rd D7 app |
| ---- | ---- | ------------ | ------------ | ------------ | ------------ |
| 998M | 109M | 317M (+208M) | 521M (+195M)	| 624M (+103M) | 739M (+115M) |
