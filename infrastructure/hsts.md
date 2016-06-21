# HSTS

HSTS (HTTP Strict Transport Security) is a security feature that lets a web site tell browsers that it should only be communicated with using HTTPS, instead of using HTTP. Read more details on <a href="https://developer.mozilla.org/en-US/docs/Web/Security/HTTP_strict_transport_security" target="_blank">Mozilla Developer Network</a>.

HSTS specification was subsequently developed to combat <a href="https://en.wikipedia.org/wiki/SSL_stripping#SSL_stripping" target="_blank">SSL stripping attacks</a>.

Applications deployed via Wodby has enabled HSTS by default (header `Strict-Transport-Security "max-age=31536000"`).

## How to disable HSTS

In case you no longer use HTTPS for your app, but your browser (Chrome) keeps redirecting you to the HTTPS version you should delete this domain from the HSTS set from the page `chrome://net-internals/#hsts`. 

Alternatively, you can use <a href="https://chrome.google.com/webstore/detail/cache-killer/jpfbieopdmepaolggioebjmedmclkbap?hl=en" target="_blank">cache killer</a> plugin.