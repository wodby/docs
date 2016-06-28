# Integration with CloudFlare

## HTTPS

If you're using SSL with CloudFlare there're 2 ways how it integration it with Wodby.

## Simple way (less secure)

1. Open your CloudFlare dashboard and navigate to the Crypto tab of your domain
2. Go to block SSL and choose Flexible mode

Done. Nothing required from the Wodby side. All traffic before CloudFlare will be secured, however the traffic between CloudFlare and Wodby will be unsecured.

## Secure way

1. Open your CloudFlare dashboard and navigate to the Crypto tab of your domain
2. Go to block SSL and choose Full (strict) mode
3. Open Wodby dashboard and navigate to the Domains tab of your instance
4. Click "Get certificate" for your domain and choose "Let's Encrypt" as provider (read <a href="/apps/domains.html#https-ssl-via-lets-encrypt">this article</a> for details)

Done. Thus, two certificates will be used: the first (on CloudFlare side) to encrypt traffic before CloudFlare and the second (Let's Encrypt) to secure traffic between CloudFlare and Wodby.