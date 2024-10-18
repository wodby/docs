# Service actions

Service can define an action that will execute an operation in an app. Such actions are accessible to run from Wodby Dashboard. Usually, it will be a kubernetes job that will run a copy of a main container with overridden `args` and/or `command` params.
