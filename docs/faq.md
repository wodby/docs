# FAQ

## How to access applications data from host

Containers persistent data can be accessed from the host server under `/srv/wodby/instances/[INSTANCE_UUID]​`

Be careful while modifying containers' files as root – it could cause unexpected permissions issues because containers have a default user different from root 

## How to upgrade my application

If you're running a vanilla application via Wodby's managed stack and this application provides an option to upgrade it via UI (like WordPress or Matomo) this option will not work because it requires a full writing permission on the entire codebase which we avoid for security reasons. The way you upgrade to a new version is by upgrading your application stack that contains this update (see stack changelog). 

If the latest version of stack does not yet have the latest version please contact us and let us know what update is missing. We usually take a more conservative position regarding updates (not counting security updates) for stability sake.

## How Wodby's availability affects my applications?

Wodby's availability does not directly affect availability of your server(s) or applications. Although if Wodby becomes unavailable some tasks such as auto deployment won't be processed and auto backups will be postponed.

You can always track our current status at http://status.wodby.com/

## Does Wodby move applications data outside my region?

Cases when your data can be moved outside of your region:
 
1. When you use Wodby Storage for backups mirroring. The location of this storage is United States. You should use your storage with the same location instead (e.g. AWS S3 bucket)

2. When you import archives from our dashboard we temporary store this data in our storage for 24 hours for further transfer. This storage never listed publicly, all URLs have huge random hash values and never published outside the dashboard

## What happens if my server IP changes?

For single server infrastructure we automatically detect new external IP. Upon the detection we update the connected server IP on Wodby and DNS records of technical domains (DNS propagation may take a few minutes). So normally, you don't need to do anything additionally. 

Infrastructure version 5.5.4 does not have this function, please contact us and we'll update your IP manually or upgrade your infrastructure

## How do I put application to maintenance mode?

You can put your app instance to maintenance from `Instance > Stack > Settings`

## How can I purchase a server?

Wodby is not a hosting provider. We believe that there are plenty of reliable providers on the market already. Instead we provide a way to connect your own server from any cloud.

## Why does team plan starts from $50?

The team plan starts with 10 [app instances](apps/instances.md) minimum. And here is why – when people use Wodby in production they expect a certain level of service which we can't provide for less than $50/mo. On the other hand we don't want to provide poor service.

Quality over quantity.

## I have a lot of applications and looking for ways to save costs

If you have many low-traffic applications we recommend consider the following:

* Do not deploy too many apps per one server because the overhead growth relatively to # of containers is not linear. ~200-300 containers is a recommended maximum
* Use dedicated (or bare-metal) server instead of VPS. It will be cheaper (but less reliable) if you know how many resources you need. You will get a guaranteed stable CPU performance unlike on VPS (cloud providers usually oversell) 
