# Cron

By default, cron runs every hour for all applications. If you want to change it connect to your main container by SSH and follow <a href="https://help.ubuntu.com/community/CronHowto#Using_Cron" target="_blank">this guide</a> to edit your crontab.

You can edit cron by executing `crontab -e`, however these changes will reset once you restart your container (happens during server reboot). We're still working on cron orchestration functionality, meanwhile you can [contact our support team](../product/support.md) to make permanent changes. 