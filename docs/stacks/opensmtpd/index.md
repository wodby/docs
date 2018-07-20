# OpenSMTPD stack documentation

!!! warning "No delivery guarantee" 
    If you're using a server from a public cloud there's 90% chance that its IP is already compromised and blacklisted by major mail services, hence your emails won't be delivered or will land in the spam folder. We **strongly recommend** using OpenSMTPD [in pair with a 3rd party SMTP server](#integration-with-3rd-party-smtp-servers).

OpenSMTPD can be configured with the following [environment variables](https://github.com/wodby/opensmtpd#environment-variables)

## Sending test emails from CLI

1. [Access](https://help.wodby.com/infrastructure/how-to-access-containers) OpenSMTPD container
2. Run `sendmail -v -f verified-sender@verified-domain.com to@example.com`
3. Enter email subject and body in the input:
  ```
  Subject: test subject

  test body
  ```
4. Enter Ctrl + D

## Integration with 3rd party SMTP servers

* [SendGrid](/integrations/sendgrid.md)
* [AWS SES](/integrations/aws.md)
* OpenSMTPD can be configured with any SMTP server. Just provide `RELAY_HOST`, `RELAY_USER` and `RELAY_PASSWORD`. By default it utilizes TLS schema with port `587` that can be changed via `RELAY_PORT`.

## Changelog

### 1.1.0

* Improved health check now runs smtp command
* Messages queue is now persistent
* Default [memory request](https://docs.wodby.com/stacks/config#resources) set to 4m

### 1.0.3

* Allow relay auth without password
* Use netcat instead of telnet in health checks
* Health check timeout increased to 30 seconds

### 1.0.2

* Bugfix: health probes caused warning in logs

### 1.0.1

* Support for relay without authentication

### 1.0.0

Initial release
