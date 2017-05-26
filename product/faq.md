# FAQ

<span id="team-plan"></span>
### Why does the team plan starts from $50?

The team plan starts with 10 [instances](../apps/instances.md) minimum. And here is why – when people use Wodby in production they expect a certain level of service which we can't provide for less than $50/mo. On the other hand we don't want to provide poor service.

Quality over quantity.

### What is instance?

Application instance is a single environment (bundle) deployed for your app (dev, staging, prod, feature, etc). Every app can have unlimited instances but at least one. Read more about instance [here](../apps/instances.md)

### How Wodby's availability affects my apps?

Wodby's availability does not affect availability of your server or apps. Although if Wodby becomes unavailable some tasks such as auto deployment won't be processed and auto backups will be postponed.   

### It's super important that all of my application's data stored in a specific region. Does Wodby anyhow store my data? 

The only case when your data can be moved outside of your region is when you use Wodby Storage for backups mirroring. The location of this storage is United States. You should use your storage with the same location instead (e.g. AWS S3 bucket).

### How can I purchase a server?

Wodby is not a hosting provider. We believe that there are plenty of reliable providers on the market already. Instead we provide a way to [connect your own server](../servers/connect/README.md) from any cloud. 

### I have a large-scale application, how can you help me?

For large-scale application we have a [container-based cluster solution](../cluster/README.md).

### It's so complex, how do I start?

Watch our <a href="https://www.youtube.com/watch?v=PMqjcU4cMPM" target="_blank">demo video</a>.
