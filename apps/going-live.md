# Going Live with Wodby

Going live process with Wodby is very simple and straightforward – you just need to create a new production [instance](instances.md) and attach your live domain: 

1. Create a new production [instance](instances.md) of your application
2. Choose a git branch (you can switch to a tag later)
3. Choose your dev/staging instance as source of database and files 
4. Choose a [server](../servers/README.md) where you want to deploy your production instance
5. Deploy the instance
6. Attach your production domain to the instance as described <a href="domains.html#attaching-custom-domain-name" target="_blank">here</a> 
7. That's it! Do not forget to enable <a href="backups.html" target="_blank">auto-backups with mirroring</a>