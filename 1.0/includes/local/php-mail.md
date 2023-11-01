By default `mailhog` service enabled to catch all outbound emails, you can switch to `opensmtpd` (uncomment corresponding service in the compose file) if you need to actually delivery emails. OpenSMTPD can be used together with a third-party SMTP service for guaranteed email delivery by providing [`RELAY_` environment variables](https://github.com/wodby/opensmtpd/#environment-variables)

By default, we use busybox's sendmail for email delivery together with enabled `mail.mixed_lf_and_crlf` php setting, however this setting has been introduced only in PHP 8.2, for older versions we use `ssmtp` (with `dos2unix` workaround). You can learn more about this setting and why we need a workaround needed in [this issue](https://github.com/php/php-src/issues/8086). The reason we don't use `ssmtp` for all versions is because this approach has issues with corrupting attachments.

For PHP 8.2+ you need the following environment variables to be set:
```
PHP_MAIL_MIXED_LF_AND_CRLF: On
PHP_SENDMAIL_PATH: '/bin/busybox sendmail -t -i -S mailhog:25'
# if you use opensmtpd
#PHP_SENDMAIL_PATH: '/bin/busybox sendmail -t -i -S mailhog:25'
```

For PHP <8.2:
```
PHP_SENDMAIL_PATH: '"/usr/bin/dos2unix -u | /usr/sbin/ssmtp -t -f"'
SSMTP_MAILHUB: mailhog:1025
# if you use opensmtpd
#SSMTP_MAILHUB: opensmtpd:25
```
