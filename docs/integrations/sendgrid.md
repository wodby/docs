# SendGrid integration

You can send emails from your applications via SendGrid by configuring mail transfer agent OpenSMTPD:

0. Make sure your application stack has enabled OpenSMTPD service
1. Log in to your SendGrid account and visit guide https://app.sendgrid.com/guide
2. Start with `Integrate using our Web API or SMTP relay` option
3. Choose `SMTP Relay`
4. Enter API Key to generate password
5. Add the following environment variables to OpenSMTPD service (replace `[Tokens]` with your values):
    ```
    RELAY_HOST=[Server]
    RELAY_USER=[Username]
    RELAY_PASSWORD=[Password]
    ```
6. Proceed to the next step in SendGrid dashboard to verify integration
7. [Send a test email](../stacks/opensmtpd/index.md#sending-test-emails-from-cli) from OpenSMTPD container
