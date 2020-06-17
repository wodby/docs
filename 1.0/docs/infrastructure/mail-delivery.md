# Mail delivery

Most of managed stack have a mail transfer agent OpenSMTPD (can be deployed as a stand-alone app) as a default mail delivery service. Emails will be sent from the server hosting your application. Additionally, you can enable mail catcher service Mailhog to catch all outbound emails and release them manually from UI to an SMTP server. You can switch an active mail delivery service from `[Instance] > Stack > Settings` page.

!!! warning "WARNING" 
    If you're using a server from a public cloud there's 90% chance that its IP is already compromised and blacklisted by major mail services, hence your emails won't be delivered or will land in the spam folder. We strongly recommend using OpenSMTPD in pair with a 3rd party SMTP server. See [OpenSMTPD stack description](../stacks/opensmtpd/index.md) to learn how.
