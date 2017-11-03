# Emails delivery from my application fails

If you're using a server from a public cloud there's 90% chance that its IP is already compromised and blacklisted by major mail services, hence your emails won't be delivered or will land in the spam folder. 

If your stack has mail transfer agent OpenSMTPD we recommend integrating it with a 3rd party email service (relay mode):

* [AWS Simple Email Service](/cloud/aws/ses.md)
* [SendGrid](/integrations/sendgrid.md)
* Any other SMTP server, see [OpenSMTPD documentation](https://cloud.wodby.com/stackhub/a545abfe-6882-4d47-b7b6-0e49516cefb7/overview)
