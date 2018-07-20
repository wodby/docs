# CloudFlare integration

## HTTPS

If you're using SSL with CloudFlare there're 2 ways how it integrate it with Wodby.

### Simple way (less secure)

* Open your CloudFlare dashboard and navigate to the Crypto tab of your domain
* Go to block SSL and choose Flexible mode
* All traffic before CloudFlare will be secured, however the traffic between CloudFlare and Wodby will be unsecured.

### Secure way

* Open your CloudFlare dashboard and navigate to the `Crypto` tab of your domain
* Go to block SSL and choose `Full (strict)` mode
* Open Wodby dashboard and navigate to the Domains tab of your instance
* Click `Get certificate` for your domain and choose `Let's Encrypt` a as provider
* Two certificates will be used: the first, on CloudFlare side, to encrypt traffic before CloudFlare and the second (Let's Encrypt) to secure traffic between CloudFlare and Wodby.