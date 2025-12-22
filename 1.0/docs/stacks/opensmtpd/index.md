# OpenSMTPD stack documentation

!!! warning "No delivery guarantee"
    If you're using a server from a public cloud there's a good chance that its IP is already compromised and blacklisted by major mail services, hence your emails will not be delivered or will land in the spam folder. We strongly recommend using OpenSMTPD [in pair with a third-party SMTP services](#integration-with-third-party-smtp-services)


OpenSMTPD can be configured with the following [environment variables](https://github.com/wodby/opensmtpd#environment-variables)

## Sending test emails from CLI

1. [Access](../../infrastructure/containers.md#accessing-containers) OpenSMTPD container
2. Run `sendmail -v -f verified-sender@verified-domain.com to@example.com`
3. Enter email subject and body in the input:
  ```
  Subject: test subject

  test body
  ```
4. Enter Ctrl + D

## Integration with third-party SMTP services

* [SendGrid](../../integrations/sendgrid.md)
* [AWS SES](../../integrations/aws.md)
* OpenSMTPD can be configured with any SMTP server. Just provide the following environment variables:
    ```
    RELAY_HOST
    RELAY_USER
    RELAY_PASSWORD
    ```
    By default, it utilizes TLS schema with port `587` that can be changed via `RELAY_PORT`.

## Changelog

This changelog is for OpenSMTPD stack on Wodby, to see image changes see tags description on [repository page](https://github.com/wodby/opensmtpd/releases).

### 2.1.4

🏔️ Updated Alpine Linux

### 2.1.3

- ⬆️ OpenSMTPD 7.6.0
- 🏔️ Updated Alpine Linux to 3.21

### 2.1.2

🏔️ Alpine Linux security updates

### 2.1.1

🏔️ Alpine Linux security updates (3.20.3)

### 2.1.0

⬆️ OpenSMTPD 7

### 2.0.4

📜 OpenSMTPD now has `$RELAY_PROTO` to change relay protocol https://github.com/wodby/opensmtpd/pull/2

### 2.0.3

🏔 Alpine Linux updated to 3.18.3, 3.16.7

### 2.0.2

🏔 Alpine Linux upgraded to 3.17.3, 3.16.5

### 2.0.1

🏔 Alpine updated to 3.17.2

### 2.0.0

- ⚠️ This version of stack requires server infrastructure 6.0.0+
- 🏔 Alpine updated to 3.17

### 1.3.1

🏔 Base OS Alpine Linux updated to 3.16.3

### 1.3.0

- ℹ️ This update requires server infrastructure at least 5.9.0
- ⬆️ OpenSMTPD 6.8.0 
- 🏔 Alpine Linux updated to 3.15

### 1.2.0

⬆️ OpenSMTPD 6.7.1 (Alpine Linux 3.13)

### 1.1.8

📦&nbsp; Base OS Alpine Linux updated to 3.10.9

### 1.1.7

- 🦴&nbsp; `ImagePullPolicy` changed to `IfNotPresent`

### 1.1.6

Alpine Linux updated to 3.11

### 1.1.5

Alpine Linux updated to 3.10.1

### 1.1.3

Alpine Linux updated to 3.9.4

### 1.1.2

Alpine Linux updated to 3.9.3

### 1.1.1

OpenSMTPD patch update to 6.0.3

### 1.1.0

* Improved health check now runs smtp command
* Messages queue is now persistent
* Default [memory request](../config.md#resources) set to 4m

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
