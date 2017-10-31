# Simple Email Service (SES)

You can send emails from your applications via SES by configuring mail transfer agent OpenSMTPD:

1. [Verify your domain](http://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-domains.html) or email address you will use to send emails from. AWS **will not** send emails from unverified sender
2. [Obtain your SMTP credentials](http://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.html)
3. Obtain SMTP Server Name from your AWS console. Open "SES > Email Sending > SMTP Setting"
4. Open OpenSMTPD service configuration window
5. Add environment variables `RELAY_HOST`, `RELAY_USER` and `RELAY_PASSWORD` with values of `Server Name`, `SMTP Username` and `Password`
6. [Send a test email from OpenSMTPD container](https://cloud.wodby.com/stackhub/a545abfe-6882-4d47-b7b6-0e49516cefb7/overview#sending-test-emails-from-cli)