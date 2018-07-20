# GitLab stack documentation

GitLab can be configured with the following [environment variables](https://github.com/wodby/gitlab#environment-variables)

## Credentials

We use email from your Wodby account as GitLab root user email. When you deploy GitLab for the first time you will be asked to change your root password.

## Backups

We do not yet provide orchestration for backup / restore from the dashboard. However, you still can do it manually. Access your GitLab (Unicorn) container and run `bundle exec rake gitlab:backup:create` to create a backup. Run `bundle exec rake gitlab:backup:restore` to restore your backup. See the [GitLab backup and restore documentation](https://docs.gitlab.com/ce/raketasks/backup_restore.html#restore-for-installation-from-source) for more details.

## SSL

Access to the gitlab application can be secured using SSL, follow these steps:

1. Add a custom domain and mark it as primary
2. Acquire an SSL certificate for this domain
3. Add an environment variable `GITLAB_HTTPS=true` to GitLab (Unicorn) and Nginx services

## Logs

All services provided with the stack configured to stream their logs to a container output. It's a common practice for docker containers. Those logs are not persistent and available until the next container restart. You can either stream logs in real-time via our dashboard or via CLI. To get logs via CLI copy `Show logs` command from `[Instance] > Stack > [Service]` and execute it on the host server of an instance. Modify `kubectl logs` command flags to your needs.

## Container registry

Follow these steps to connect docker container registry to your GitLab instance:

1. Enable Docker registry service in your application stack
2. Assign a custom domain to Docker registry from Domains tab
3. Acquire Let's Encrypt certificate for this domain
4. Add the following environment variables (replace [TOKEN]) to GitLab (Unicorn) service in your stack and redeploy it:
  ```
  GITLAB_REGISTRY_ENABLED: true
  GITLAB_REGISTRY_HOST: [YOUR REGISTRY DOMAIN (e.g. registry.example.com)]
  ```
5. Once the deployment from the previous step has completed, add the following environment variables (replace [TOKEN]) to your Docker registry service:
  ```
  REGISTRY_AUTH_TOKEN_ROOTCERTBUNDLE: /certs/registry-auth.crt
  REGISTRY_AUTH_TOKEN_REALM: http://[YOUR GITLAB PRIMARY DOMAIN]/jwt/auth
  REGISTRY_AUTH_TOKEN_SERVICE: container_registry
  REGISTRY_AUTH_TOKEN_ISSUER: gitlab-issuer
  ```

## GitLab CI

Deploy a new [GitLab Runner](https://cloud.wodby.com/stackhub/e448dc7b-a570-430a-8415-12a874c67629/overview) application. The runner will use `docker` executor by default. Add the following environment variables to register your runner in your Gitlab instance:

```
CI_SERVER_URL: [YOUR GITLAB URL]
REGISTRATION_TOKEN: [YOUR GITLAB REGISTRATION TOKEN]
```

You can find the token from `/admin/runners` if you want to register it as a shared runner. Or visit `Settings -> CI/CD` page of your GitLab project to register it as a specific.


## GitLab runner

Add `CI_SERVER_URL` and `REGISTRATION_TOKEN` environment variables to register your runner in your Gitlab instance. All environment variables available for configuration can be found at https://github.com/wodby/gitlab-runner

## Known issues

GitLab is not designed to be run with a "one process per container" approach. As a result some functionality may not be available, such as

* GitLab can't detect Sidekiq background jobs (e.g. `Admin Area > Background Jobs`)
* Logs (`Admin Area > Logs`) not available, but you still can get logs from containers' output via Wodby dashboard

## Mail delivery

Mail transfer agent [OpenSMTPD](../opensmtpd/index.md) included in the stack and used as a default mail delivery service. Emails will be sent from the server hosting your application. 

## GitLab Pages

Prerequisites:

* You have a custom domain your gitlab pages will be served under (e.g. *.example.io)
* You have configured a wildcard DNS record for that domain
* You have connected at least one shared [GitLab Runner](#gitlab-runner)

Follow these steps to connect docker container registry to your GitLab instance:

1. Enable GitLab Pages service in your application stack
2. Add your custom wildcard domain with * (e.g. *.example.io), attach it to pages service
3. Add the following environment variables to GitLab (Unicorn) service of your stack:
```
  GITLAB_PAGES_ENABLED: true
  GITLAB_PAGES_HOST: [YOUR CUSTOM DOMAIN WITHOUT * (e.g. example.io)]
```
4. Redeploy your stack
5. Deploy your GitLab pages repository (you can fork one of the [official examples](https://gitlab.com/pages))
6. Manually run a pipeline for the first time in order to trigger the job process
7. If the job has completed successfully, you can find your pages domain under your project's `Settings > Pages`

For more details visit https://about.gitlab.com/features/pages/

## Reply by email

GitLab can be set up to allow users to comment on issues and merge requests by replying to notification emails. Learn more about this feature from [the official documentation](https://docs.gitlab.com/ce/administration/reply_by_email.html).

To enable this functionality you should:

1. Enable Mailroom service in your stack
2. Add environment variables listed below to `GitLab` (Unicorn) service:

| Variable                       | Description |
| ------------------------------ | ----------- |
| GITLAB_INCOMING_EMAIL          | Set to `true` to enable |
| GITLAB_INCOMING_EMAIL_ADDRESS  | The email address including the `%{key}` placeholder that will be replaced to reference the item being replied to. The placeholder can be omitted but if present, it must appear in the "user" part of the address (before the `@`). |
| GITLAB_INCOMING_EMAIL_USER     | Email account username. With third party providers, this is usually the full email address. With self-hosted email servers, this is usually the user part of the email address. |
| GITLAB_INCOMING_EMAIL_PASSWORD | Email account password |
| GITLAB_INCOMING_EMAIL_HOST     | IMAP server host |
| GITLAB_INCOMING_EMAIL_PORT     | IMAP server port |

### Gmail

If you want to use Gmail / Google Apps with Reply by email, make sure you have IMAP access enabled. Configuration for Gmail / Google Apps, assumes mailbox `gitlab-incoming@gmail.com`:

```
GITLAB_INCOMING_EMAIL: true
GITLAB_INCOMING_EMAIL_ADDRESS: gitlab-incoming+%{key}@gmail.com
GITLAB_INCOMING_EMAIL_USER: gitlab-incoming@gmail.com
GITLAB_INCOMING_EMAIL_PASSWORD: my-password
GITLAB_INCOMING_EMAIL_HOST: imap.gmail.com
GITLAB_INCOMING_EMAIL_PORT: 993
```

### Microsoft Exchange

Configuration for Microsoft Exchange mail server with IMAP enabled, assumes mailbox `incoming@exchange.example.com`:


```
GITLAB_INCOMING_EMAIL: true
GITLAB_INCOMING_EMAIL_ADDRESS: incoming@exchange.example.com
GITLAB_INCOMING_EMAIL_USER: incoming@ad-domain.example.com
GITLAB_INCOMING_EMAIL_PASSWORD: my-password
GITLAB_INCOMING_EMAIL_HOST: exchange.example.com
GITLAB_INCOMING_EMAIL_PORT: 993
```
