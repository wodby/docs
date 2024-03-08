By default `mailhog` service enabled to catch all outbound emails, you can switch to `opensmtpd` (uncomment corresponding service in the compose file) if you need to actually delivery emails. OpenSMTPD can be used together with a third-party SMTP service for guaranteed email delivery by providing [`RELAY_` environment variables](https://github.com/wodby/opensmtpd/#environment-variables)

We use msmtp for email delivery, PHP 8.2+ has `mail.mixed_lf_and_crlf`, PHP 8.1 and previous versions need to use `dos2unix` workaround. You can learn more about this setting and why we need a workaround needed in [this issue](https://github.com/php/php-src/issues/8086). 

For PHP 8.2+ you need the following environment variables to be set:
```
PHP_MAIL_MIXED_LF_AND_CRLF: On
PHP_SENDMAIL_PATH: '/bin/bin/msmtp -t'
MSMTP_HOST: mailhog
MSMTP_PORT: 1025
```

For PHP 8.1 and previous:
```
PHP_SENDMAIL_PATH: '"/usr/bin/dos2unix -u | /usr/bin/msmtp -t"'
MSMTP_HOST: mailhog
MSMTP_PORT: 1025
```

If you want to use OpenSMTPD replace the following env vars:
```
MSMTP_HOST: opensmtpd
MSMTP_PORT: 25
```
