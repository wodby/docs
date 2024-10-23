# Integration provider

Provider is the representation of Wodby's integration with third-party services. One provider can have multiple [integration types](types.md) that can optionally be selected when a new integration created. 

Except generic [variable integration](variable.md) all providers have a certain implementation logic depending on their type, for example for providers with kubernetes integration Wodby offers native-integration with the cloud services that provide managed Kubernetes solution.

Only _variable_ providers can be created by users, all others provided by Wodby. If you miss a certain provider feel free to [contact us](../support.md) and suggest. 
