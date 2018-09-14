Rsyslog can be used to stream your applications logs. It's similar to using syslog, however there's no syslog in PHP container (one process per container). Rsyslog will stream all incoming logs to a container output.

You can use [Monolog](https://packagist.org/packages/monolog/monolog) with `SyslogUdpHandler` to stream logs to rsyslog.