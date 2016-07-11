# Mail Transfer Agent (SMTP)

## Overview

### Before 3.3.0

Wodby infrastructure includes <a href="https://www.opensmtpd.org/" target="_blank">OpenSMTPD</a> per each server. Every application instance has <a href="http://msmtp.sourceforge.net/">msmtp</a> client installed contacting OpenSMTPD server.
 
### Since <a href="versioning.html#330">3.3.0</a>

Every web container has postfix server. Configuration files located in `/srv/conf/postfix`. 

## Guaranteed delivery of transaction emails

To make sure your transaction emails will be guaranteed delivered we recommend to use Transaction email services such as:

* <a href="http://sendgrid.com/" target="_blank">SendGrid</a> (has a free version). Read <a href="http://atendesigngroup.com/blog/send-mail-drupal-7-deliver-email-reliably-avoid-spam-folder" target="_blank">this article</a> on how to integration SendGrid with Drupal
* <a href="https://aws.amazon.com/ses/" target="_blank">AWS SES</a>
* <a href="http://mailchimp.com/" target="_blank">Mailchimp</a>