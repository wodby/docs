# SendGrid

You can send emails from your applications via SendGrid by configuring mail transfer agent OpenSMTPD:

1. Log in to your SendGrid account and visit guide https://app.sendgrid.com/guide
2. Start with `Integrate using our Web API or SMTP relay` option
3. Choose `SMTP Relay`
4. Enter API Key to generate password
5. Open OpenSMTPD service configuration window
6. Add environment variables `RELAY_HOST`, `RELAY_USER` and `RELAY_PASSWORD` with values of `Server`, `Username` and `Password` from SendGrid
7. Proceed to the next step in SendGrid dashboard to verify integration
6. [Send a test email from OpenSMTPD container](https://cloud.wodby.com/stackhub/a545abfe-6882-4d47-b7b6-0e49516cefb7/overview#sending-test-emails-from-cli)
