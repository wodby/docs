# Service endpoints

Services that provide public ports can define endpoints. An endpoint is the collection of ports and domains. Services can define only ports in their manifests, domains can be added later after app creation.

An endpoint designed to represent a single kubernetes service. 

There are three type of ports:
1. `http` - such ports allow domains with TLS certificates to be attached
2. `udp` - such ports can be publicly exposed
3. `tcp` - such ports can be publicly exposed

One port per endpoint can be marked as main. When `http` port marked as main in the main endpoint, a main technical domain will be attached to it during app creation.
