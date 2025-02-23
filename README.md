<p  align = "center"><img  alt="Secweb logo"  src="https://raw.githubusercontent.com/tmotagam/Secweb/main/Secweb.jpg"></p>
<p  align="center"><em>Secweb helps in setting security headers for FastApi and Starlette</em></p>

---

Secweb is the pack of middlewares for setting security headers for fastapi and can also be used for any framework created on starlette it has 16 middlewares for setting headers of your website and also for your api(s).

**The PermissionsPolicy middleware lies in development branch [here](https://github.com/tmotagam/Secweb/tree/Secweb-Beta#readme)**

### Features

- Lightweight and fast
  <br>

- No External dependency
  <br>

- Use recommended headers from OWASP and MDN
  <br>

- Recommended by OWASP

The list of middleware is as follows:

1. Content Security Policy (CSP)
   <br>

2. Origin Agent Cluster
   <br>

3. Referrer Policy
   <br>

4. HTTP Strict Transport Security(HSTS)
   <br>

5. HTTP Strict Transport Security(HSTS) for WebSockets
   <br>

6. X-Content-Type-Options
   <br>

7. X-DNS-Prefetch-Control
   <br>

8. X-Download-Options
   <br>

9. X-Frame
   <br>

10. X-Permitted-Cross-Domain-Policies
    <br>

11. X-XSS-Protection
    <br>

12. Cross-Origin-Embedder-Policy
    <br>

13. Cross-Origin-Opener-Policy
    <br>

14. Cross-Origin-Resource-Policy
    <br>

15. Clear-Site-Data
    <br>

16. Cache-Control

# Requirements

- [Python >= 3.7](https://www.python.org/downloads/)
- [Starlette](https://pypi.org/project/starlette/)

# Installation

```powershell
pip install Secweb
```

# Usage

The package Secweb can be used in two different ways:

1. Use the SecWeb class - it includes all the 16 classes together
   <br>

2. Use the 16 middleware classes separately

## SecWeb class

```Python
from Secweb import SecWeb

SecWeb(app=app) # The app is the ASGIapp required by the starlette to give access to the different methods to the class
```

The above example uses all the default headers value that are preset. You can change the values by creating the option dict.

You can also set flags for nonce generation for csp header using the `script_nonce=True` and `style_nonce=True` flags. The `report_only` flag is added for csp report only header. For Clear-Site-Data header `Routes=[]` array is used for applying the header, it is empty by default.

```Python
from Secweb import SecWeb

SecWeb(app=app, Option={'referrer': ['no-referrer']}, Routes=[], script_nonce=False, style_nonce=False, report_only=False)
```

The `Option`-parameter uses 16 keys for calling middleware classes to set the user-defined policies or activating or deactivating headers.

**Note: Activating/Deactivating the header can only be done in SecWeb class in Option param**

```Python
from Secweb import SecWeb

Secweb(app=app, Option={'referrer': False, 'xframe': False})
```

The values are as follows:

1. `'csp'` for calling ContentSecurityPolicy class to set the user-defined values or activate/deactivate the header
   <br>

2. `'referrer'` for calling ReferrerPolicy class to set the user-defined values or activate/deactivate the header
   <br>

3. `'xdns'` for calling XDNSPrefetchControl class to set the user-defined values or activate/deactivate the header
   <br>

4. `'xcdp'` for calling XPermittedCrossDomainPolicies class to set the user-defined values or activate/deactivate the header
   <br>

5. `'hsts'` for calling HSTS class to set the user-defined values or activate/deactivate the header
   <br>

6. `'wshsts'` for calling WsHSTS class to set the user-defined values for Websockets or activate/deactivate the header
   <br>

7. `'xframe'` for calling XFrame class to set the user-defined values or activate/deactivate the header
   <br>

8. `'coep'` for calling CrossOriginEmbedderPolicy class to set the user-defined values or activate/deactivate the header
   <br>

9. `'coop'` for calling CrossOriginOpenerPolicy class to set the user-defined values or activate/deactivate the header
   <br>

10. `'corp'` for calling CrossOriginResourcePolicy class to set the user-defined values or activate/deactivate the header
    <br>

11. `'clearSiteData'` for calling ClearSiteData class to set the user-defined values or activate/deactivate the header
    <br>

12. `'cacheControl'` for calling CacheControl class to set the user-defined values or activate/deactivate the header
    <br>

13. `'xcto'` for activating/deactivating X-Content-Type-Options header
    <br>

14. `'xdo'` for activating/deactivating X-Download-Options header
    <br>

15. `'xss'` for activating/deactivating x-xss-protection header
    <br>

16. `'oac'` for activating/deactivating Origin-Agent-Cluster header

```python
# Example of all values

SecWeb(app=app, Option={'csp': {'default-src': ["'self'"]}, 'xframe':'SAMEORIGIN', 'hsts': {'max-age': 4, 'preload': True}, 'wshsts': {'max-age': 10, 'preload': True},'xcdp': 'all', 'xdns': 'on', 'referrer': ['no-referrer'], 'coep':'require-corp', 'coop':'same-origin-allow-popups', 'corp': 'same-site', 'clearSiteData': {'cache': True, 'storage': True}, 'cacheControl': {'public': True, 's-maxage': 600}, 'xss': False}, Routes=['/login/{id}', '/logout/{id:uuid}/username/{username:string}'])
```

## Middleware Classes

### Content Security Policy (CSP)

#### Nonce Processor

The Nonce_Processor module generates nonce for csp header

```python
# Some Code

nonce = Nonce_Processor(DEFAULT_ENTROPY=90) # inject the nonce variable into the jinja or html

# Some Code
```

`DEFAULT_ENTROPY` is used to set the nonce length.

The nonce processor needs to be called on the route the following example is of FastApi calling the nonce processor on the route

```python

from fastapi import FastAPI
from Secweb.ContentSecurityPolicy import Nonce_Processor

app = FastAPI()

@app.get("/")

async  def  root():

# some code

nonce = Nonce_Processor(DEFAULT_ENTROPY=90) # inject the nonce variable into the jinja or html

# some more code
```

ContentSecurityPolicy class sets the csp header.

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb.ContentSecurityPolicy import Nonce_Processor

app = FastAPI()

app.add_middleware(ContentSecurityPolicy, Option={'default-src': ["'self'"], 'base-uri': ["'self'"], 'block-all-mixed-content': []}, script_nonce=False, style_nonce=False, report_only=False)
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb.ContentSecurityPolicy import Nonce_Processor


app = Starlette()

app.add_middleware(ContentSecurityPolicy, Option={'default-src': ["'self'"], 'base-uri': ["'self'"], 'block-all-mixed-content': []}, script_nonce=False, style_nonce=False, report_only=False)
```

- `script_nonce=False`: nonce flag for inline Javascript
- `style_nonce=False`: nonce flag for inline css
- `report_only=False`: report only flag which makes csp report only header

For more detail on CSP header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy).

For more detail on CSP-report-only header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy-Report-Only).

### Origin Agent Cluster

OriginAgentCluster class sets the Origin-Agent-Cluster header. It takes no parameters.

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb.OriginAgentCluster import OriginAgentCluster

app = FastAPI()
app.add_middleware(OriginAgentCluster)
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb.OriginAgentCluster import OriginAgentCluster

app = Starlette()

app.add_middleware(OriginAgentCluster)
```

For more detail on Origin-Agent-Cluster header go to [WHATWG Site](https://html.spec.whatwg.org/multipage/origin.html#origin-keyed-agent-clusters).

### Referrer Policy

ReferrerPolicy class sets the Referrer-Policy header

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb.ReferrerPolicy import ReferrerPolicy

app = FastAPI()

app.add_middleware(ReferrerPolicy, Option=['strict-origin-when-cross-origin'])
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb.ReferrerPolicy import ReferrerPolicy

app = Starlette()
app.add_middleware(ReferrerPolicy, Option=['strict-origin-when-cross-origin'])
```

For more detail on Referrer-Policy header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy).

### HTTP Strict Transport Security (HSTS)

HSTS class sets the Strict-Transport-Security header

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb.StrictTransportSecurity import HSTS

app = FastAPI()

app.add_middleware(HSTS, Option={'max-age': 4, 'preload': True})
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb.StrictTransportSecurity import HSTS

app = Starlette()

app.add_middleware(HSTS, Option={'max-age': 4, 'preload': True})
```

For more detail on Strict-Transport-Security header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security).

### HTTP Strict Transport Security (HSTS) for WebSockets

HSTS class sets the Strict-Transport-Security header for Websockets

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb.WsStrictTransportSecurity import WsHSTS

app = FastAPI()

app.add_middleware(WsHSTS, Option={'max-age': 4, 'preload': True})
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb.WsStrictTransportSecurity import WsHSTS

app = Starlette()

app.add_middleware(WsHSTS, Option={'max-age': 4, 'preload': True})
```

For more detail on Strict-Transport-Security header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security).

### X-Content-Type-Options

XContentTypeOptions class sets the X-Content-Type-Options header the class takes no parameters

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb.XContentTypeOptions import XContentTypeOptions

app = FastAPI()

app.add_middleware(XContentTypeOptions)
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb.XContentTypeOptions import XContentTypeOptions

app = Starlette()

app.add_middleware(XContentTypeOptions)
```

For more detail on X-Content-Type-Options header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options).

### X-DNS-Prefetch-Control

XDNSPrefetchControl class sets the X-DNS-Prefetch-Control header

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb.XDNSPrefetchControl import XDNSPrefetchControl

app = FastAPI()

app.add_middleware(XDNSPrefetchControl, Option='on')
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb.XDNSPrefetchControl import XDNSPrefetchControl

app = Starlette()

app.add_middleware(XDNSPrefetchControl, Option='off')
```

For more detail on X-DNS-Prefetch-Control header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-DNS-Prefetch-Control).

### X-Download-Options

XDownloadOptions class sets the X-Download-Options header the class takes no parameter

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb.XDownloadOptions import XDownloadOptions

app = FastAPI()

app.add_middleware(XDownloadOptions)
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb.XDownloadOptions import XDownloadOptions

app = Starlette()

app.add_middleware(XDownloadOptions)
```

### X-Frame

XFrame class sets the X-Frame-Options header

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb.XFrameOptions import XFrame

app = FastAPI()

app.add_middleware(XFrame, Option='DENY')
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb.XFrameOptions import XFrame

app = Starlette()

app.add_middleware(XFrame, Option='DENY')
```

For more detail on X-Frame-Options header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options).

### X-Permitted-Cross-Domain-Policies

XPermittedCrossDomainPolicies class sets the X-Permitted-Cross-Domain-Policies header

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb.XPermittedCrossDomainPolicies import XPermittedCrossDomainPolicies

app = FastAPI()

app.add_middleware(XPermittedCrossDomainPolicies, Option='none')
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb.XPermittedCrossDomainPolicies import XPermittedCrossDomainPolicies

app = Starlette()

app.add_middleware(XPermittedCrossDomainPolicies, Option='none')
```

For more detail on X-Permitted-Cross-Domain-Policies header go to [OWASP Site](https://owasp.org/www-project-secure-headers/#x-permitted-cross-domain-policies).

### X-XSS-Protection

xXSSProtection class sets the X-XSS-Protection header the class takes no parameter

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb.xXSSProtection import xXSSProtection

app = FastAPI()

app.add_middleware(xXSSProtection)
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb.xXSSProtection import xXSSProtection

app = Starlette()

app.add_middleware(xXSSProtection)
```

For more detail on X-XSS-Protection header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection).

### Cross Origin Embedder Policy

CrossOriginEmbedderPolicy class sets the Cross Origin Embedder Policy header

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb.CrossOriginEmbedderPolicy import CrossOriginEmbedderPolicy

app = FastAPI()

app.add_middleware(CrossOriginEmbedderPolicy, Option='unsafe-none')
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb.CrossOriginEmbedderPolicy import CrossOriginEmbedderPolicy

app = Starlette()

app.add_middleware(CrossOriginEmbedderPolicy, Option='unsafe-none')
```

For more detail on Cross Origin Embedder Policy header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy).

### Cross Origin Opener Policy

CrossOriginOpenerPolicy class sets the Cross Origin Opener Policy header

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb.CrossOriginOpenerPolicy import CrossOriginOpenerPolicy

app = FastAPI()

app.add_middleware(CrossOriginOpenerPolicy, Option='unsafe-none')
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb.CrossOriginOpenerPolicy import CrossOriginOpenerPolicy

app = Starlette()

app.add_middleware(CrossOriginOpenerPolicy, Option='unsafe-none')
```

For more detail on Cross Origin Opener Policy header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy).

### Cross Origin Resource Policy

CrossOriginResourcePolicy class sets the Cross Origin Resource Policy header

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb.CrossOriginResourcePolicy import CrossOriginResourcePolicy

app = FastAPI()

app.add_middleware(CrossOriginResourcePolicy, Option='same-site')
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb.CrossOriginResourcePolicy import CrossOriginResourcePolicy

app = Starlette()

app.add_middleware(CrossOriginResourcePolicy, Option='same-site')
```

For more detail on Cross Origin Resource Policy header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Resource-Policy).

### Clear Site Data

ClearSiteData class sets the Clear-Site-Data header. In this class the routes array is compulsory so that the header can only be applied to the specified route as it clears every data on the users browser you can add static, dynamic routes like shown below.

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb.ClearSiteData import ClearSiteData

app = FastAPI()

app.add_middleware(ClearSiteData, Option={'cookies': True}, Routes=['/login', '/logout/{id}'])
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb.ClearSiteData import ClearSiteData

app = Starlette()

app.add_middleware(ClearSiteData, Option={'cookies': True}, Routes=['/login', '/logout/{id}'])
```

For more detail on Clear Site Data Header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Clear-Site-Data).

### Cache Control

CacheControl class sets the Cache-Control header. This is useful for controlling cached data on user`s browser

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb.CacheControl import CacheControl

app = FastAPI()

app.add_middleware(CacheControl, Option={'s-maxage': 600, 'public': True})
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb.CacheControl import CacheControl

app = Starlette()

app.add_middleware(CacheControl, Option={'s-maxage': 600, 'public': True})
```

For more detail on Cache Control Header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control).

# Contributing

Pull requests and Issues are welcome. For major changes, please open an issue first to discuss what you would like to change.

[Github](https://github.com/tmotagam/Secweb)

# License

[MLP 2.0](https://www.mozilla.org/en-US/MPL/2.0/)

# Secweb Icon

[Secweb Icon](https://github.com/tmotagam/Secweb/blob/main/Secweb.jpg) © 2021 - 2025 by [Motagamwala Taha Arif Ali](https://github.com/tmotagam) is licensed under [Attribution-NonCommercial-NoDerivatives 4.0 International](https://creativecommons.org/licenses/by-nc-nd/4.0/?ref=chooser-v1)
