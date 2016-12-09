# Mail Transfer Agent (SMTP)

## Overview

By default [bundles](../bundles/README.md) include [OpenSMTPD container](../bundles/containers/opensmtpd.md). Additionally, you can catch all your emails by deploying optional [Mailhog container](../bundles/containers/mailhog.md). 
 
## Guaranteed delivery of transaction emails

To make sure your transaction emails will be guaranteed delivered we recommend to use Transaction email services such as:

* <a href="http://sendgrid.com/" target="_blank">SendGrid</a> (has a free version). Read <a href="http://atendesigngroup.com/blog/send-mail-drupal-7-deliver-email-reliably-avoid-spam-folder" target="_blank">this article</a> on how to integration SendGrid with Drupal
* <a href="https://aws.amazon.com/ses/" target="_blank">AWS SES</a>
* <a href="http://mailchimp.com/" target="_blank">Mailchimp</a>