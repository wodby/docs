# AWS

## Connecting EC2 node 

Currently, we don't have a native integration with AWS. But you still can connect your server by following these steps: 

0. Learn [requirements and recommendations](../infrastructure/connecting-server.md#requirements-and-recommendations)

1. Login to your AWS Console
 
2. Choose EC2 (Virtual Servers in the Cloud)

3. Choose `Instances > Click "Launch Instance"`

4. Choose an image (AMI) from the list of [supported OS](../infrastructure/connecting-server.md#supported-os)

5. Choose an instance type. **Do not** use `t2` (burstable performance) instances unless you know what you're doing

6. Go to `4. Add Storage` (vertical tabs) and set `Size (GiB)` to at least `20`

7. Go to `6. Configure Security Group`. Besides the default SSH rule (port 22), add the following rules: HTTP, HTTPS and custom TCP rule with the range 31222-32222 as shown below:

![](../assets/aws-security-groups.png)

8. Click `Review and Launch`

9. Now it's all set on AWS side. Now connect the server (`Servers > Connect > AWS`) and follow the instructions

## Sending emails via Simple Email Service (SES)

You can send emails from your applications via SES by configuring mail transfer agent OpenSMTPD:

0. Make sure your application stack has enabled OpenSMTPD service
1. [Verify your domain](http://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-domains.html) or email address you will use to send emails from. AWS **will not** send emails from unverified sender
2. [Obtain your SMTP credentials](http://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.html)
3. Obtain SMTP Server Name from your AWS console. Open "SES > Email Sending > SMTP Setting"
4. Add the following environment variables to OpenSMTPD service (replace `[Tokens]` with your values):
    ```
    RELAY_HOST=[Server Name]
    RELAY_USER=[SMTP Username]
    RELAY_PASSWORD=[Password]
    ```
5. [Send a test email](../stacks/opensmtpd/index.md#sending-test-emails-from-cli) from OpenSMTPD container

## Backups mirroring to Simple Safe Storage (S3)

For stacks providing [backups orchestration](../apps/backups.md) you can set up backups mirroring to your own AWS S3 bucket. Enable backups mirroring from `Instance > Backups > Mirroing` page and specify AWS credentials:

* AWS Access Key Id
* AWS Secret Access Key
* Bucket name
* Bucket region
