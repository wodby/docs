By default `mailpit` service enabled to catch all outbound emails, you can switch to `opensmtpd` (uncomment corresponding service in the compose file) if you need to actually delivery emails. OpenSMTPD can be used together with a third-party SMTP service for guaranteed email delivery by providing [`RELAY_` environment variables](https://github.com/wodby/opensmtpd/#environment-variables)

If you want to use OpenSMTPD replace the following env vars:
```
MSMTP_HOST: opensmtpd
MSMTP_PORT: 25
```
