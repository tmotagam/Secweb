<p align = "center"><img alt="Secweb logo" src="https://raw.githubusercontent.com/tmotagam/Secweb/main/Secweb.jpg"></p>

<p align="center"><em>Secweb helps in setting security headers for FastApi and Starlette</em></p>

---
<br>

## :warning: This is a Dev Version Readme.

Secweb is the pack of middlewares for setting security headers for fastapi and can also be used for any framework created on starlette it has 12 middlewares for setting headers of your website and also for your api`s

The list of middleware is as follows:

1. Content Security Policy (CSP)
<br>

2. ExpectCT
<br>

3. Origin Agent Cluster
<br>

4. Referrer Policy
<br>

5. HTTP Strict Transport Security(HSTS)
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

12. Permissions Policy

## Requirements

* [Python >= 3.6](https://www.python.org/downloads/)

* [Starlette](https://pypi.org/project/starlette/)

## Installation

To install the dev version of the Secweb you have to download the .whl file from build directory in this branch and install the Secweb

```powershell
pip install Secweb_dev-1.0.0-py3-none-any.whl
```
## Usage
The package Secweb can be used in two different ways

1. To use SecWeb class it includes all the 12 classes together
<br>

2. To use the 12 middleware classes separately
<br>

### SecWeb class

```Python
from Secweb import SecWeb

SecWeb(app=app)  # The app is the ASGIapp required by the starlette to give access to the different methods to the class
```
The above example uses all the default headers value that are are preset you can change the values by creating the option dict you can also set flags for nonce generation for csp header using the `script_nonce=True` and `style_nonce=True` flags

```Python
from Secweb import SecWeb

SecWeb(app=app, Option={'referrer': {'Referrer-Policy': 'no-referrer'}}, script_nonce=False, style_nonce=False)
```
The Option uses 9 keys for calling middleware classes to set the user-defined policies. 3 middleware classes doesn`t take any values.

The values are as follows:

1. `'csp'` for calling ContentSecurityPolicy class to set the user-defined values
<br>

2. `'expectCt'` for calling ExpectCt class to set the user-defined values
<br>

3. `'referrer'` for calling ReferrerPolicy class to set the user-defined values
<br>

4. `'xdns'` for calling XDNSPrefetchControl class to set the user-defined values
<br>

5. `'xcdp'` for calling XPermittedCrossDomainPolicies class to set the user-defined values
<br>

6. `'hsts'` for calling HSTS class to set the user-defined values
<br>

7. `'xss'` for calling xXSSProtection class to set the user-defined values
<br>

8. `'xframe'` for calling XFrame class to set the user-defined values
<br>

9. `'PermissionPolicy'` for calling the PermissionsPolicy class to set the user-defined values

```python
# Example of the values
SecWeb(app=app, Option={'csp': {'default-src': ["'self'"]}, 'xframe': {'X-Frame-Options': 'SAMEORIGIN'}, 'xss': {'X-XSS-Protection': '1; mode=block'}, 'hsts': {'max-age': 4, 'preload': True}, 'xcdp': {'X-Permitted-Cross-Domain-Policies': 'all'}, 'xdns': {'X-DNS-Prefetch-Control': 'on'}, 'referrer': {'Referrer-Policy': 'no-referrer'}, 'expectCt': {'max-age': 128, 'enforce': True, 'report-uri': "https://example.com/example"}, 'PermissionPolicy': {'accelerometer': ['self', '"https://example.com/"'], 'document-domain': ['*']'}})
```
### Middleware Classes

#### Content Security Policy (CSP)

ContentSecurityPolicy class sets the csp header

The Nonce_Processor module generates nonce for csp header

Nonce Processor

```python
    # Some Code
    nonce = Nonce_Processor(DEFAULT_ENTROPY=20)  # inject the nonce variable into the jinja or html
    # Some Code
```
DEFAULT_ENTROPY is used to set the nonce length.
The nonce processor needs to be called on the route the following example is of FastApi calling the nonce processor on the route

```python
from fastapi import FastAPI
from Secweb.ContentSecurityPolicy import Nonce_Processor

app = FastAPI()


@app.get("/")
async def root():
    # some code
    nonce = Nonce_Processor(DEFAULT_ENTROPY=20)  # inject the nonce variable into the jinja or html
    # some more code
```
ContentSecurityPolicy

This is for the FastApi

```python
from fastapi import FastAPI
from Secweb.ContentSecurityPolicy import Nonce_Processor

app = FastAPI()

app.add_middleware(ContentSecurityPolicy, Option={'default-src': ["'self'"], 'base-uri': ["'self'"], 'block-all-mixed-content': []}, script_nonce=False, style_nonce=False)
```

This is for the Starlette

```python
from starlette.applications import Starlette
from Secweb.ContentSecurityPolicy import Nonce_Processor

app = Starlette()

app.add_middleware(ContentSecurityPolicy, Option={'default-src': ["'self'"], 'base-uri': ["'self'"], 'block-all-mixed-content': []}, script_nonce=False, style_nonce=False)
```
script_nonce=False This is the nonce flag for inline Js

style_nonce=False This is the nonce flag for inline css

For more detail on CSP header go to this [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy)

#### ExpectCT

ExpectCt class sets the ExpectCt header

```python
from fastapi import FastAPI
from Secweb.ExpectCt import ExpectCt

app = FastAPI()

app.add_middleware(ExpectCt, Option={'max-age': 128, 'enforce': True, 'report-uri': "https://example.com/example"})

# OR
from starlette.applications import Starlette
from Secweb.ExpectCt import ExpectCt

app = Starlette()

app.add_middleware(ExpectCt, Option={'max-age': 128, 'enforce': True, 'report-uri': "https://example.com/example"})
```
For more detail on ExpectCt header go to this [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Expect-CT)

#### Origin Agent Cluster

OriginAgentCluster class sets the Origin-Agent-Cluster header the class takes no parameters

```python
from fastapi import FastAPI
from Secweb.OriginAgentCluster import OriginAgentCluster

app = FastAPI()

app.add_middleware(OriginAgentCluster)

# OR

from starlette.applications import Starlette
from Secweb.OriginAgentCluster import OriginAgentCluster

app = Starlette()

app.add_middleware(OriginAgentCluster)
```
For more detail on Origin-Agent-Cluster header go to this [WHATWG Site](https://html.spec.whatwg.org/multipage/origin.html#origin-keyed-agent-clusters)

#### Referrer Policy

ReferrerPolicy class sets the Referrer-Policy header

```python
from fastapi import FastAPI
from Secweb.ReferrerPolicy import ReferrerPolicy

app = FastAPI()

app.add_middleware(ReferrerPolicy, Option={'Referrer-Policy': 'strict-origin-when-cross-origin'})

# OR

from starlette.applications import Starlette
from Secweb.ReferrerPolicy import ReferrerPolicy

app = Starlette()

app.add_middleware(ReferrerPolicy, Option={'Referrer-Policy': 'strict-origin-when-cross-origin'})
```
For more detail on Referrer-Policy header go to this [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy)

#### HTTP Strict Transport Security (HSTS)

HSTS class sets the Strict-Transport-Security header

```python
from fastapi import FastAPI
from Secweb.StrictTransportSecurity import HSTS

app = FastAPI()

app.add_middleware(HSTS, Option={'max-age': 4, 'preload': True})

# OR

from starlette.applications import Starlette
from Secweb.StrictTransportSecurity import HSTS

app = Starlette()

app.add_middleware(HSTS, Option={'max-age': 4, 'preload': True})
```
For more detail on Strict-Transport-Security header go to this [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security)

#### X-Content-Type-Options

XContentTypeOptions class sets the X-Content-Type-Options header the class takes no parameters

```python
from fastapi import FastAPI
from Secweb.XContentTypeOptions import XContentTypeOptions

app = FastAPI()

app.add_middleware(XContentTypeOptions)

# OR

from starlette.applications import Starlette
from Secweb.XContentTypeOptions import XContentTypeOptions

app = Starlette()

app.add_middleware(XContentTypeOptions)
```
For more detail on X-Content-Type-Options header go to this [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options)

#### X-DNS-Prefetch-Control

XDNSPrefetchControl class sets the X-DNS-Prefetch-Control header

```python
from fastapi import FastAPI
from Secweb.XDNSPrefetchControl import XDNSPrefetchControl

app = FastAPI()

app.add_middleware(XDNSPrefetchControl, Option={'X-DNS-Prefetch-Control': 'on'})

# OR

from starlette.applications import Starlette
from Secweb.XDNSPrefetchControl import XDNSPrefetchControl

app = Starlette()

app.add_middleware(XDNSPrefetchControl, Option={'X-DNS-Prefetch-Control': 'off'})
```
For more detail on X-DNS-Prefetch-Control header go to this [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-DNS-Prefetch-Control)

#### X-Download-Options

XDownloadOptions class sets the X-Download-Options header the class takes no parameter

```python
from fastapi import FastAPI
from Secweb.XDownloadOptions import XDownloadOptions

app = FastAPI()

app.add_middleware(XDownloadOptions)

# OR

from starlette.applications import Starlette
from Secweb.XDownloadOptions import XDownloadOptions

app = Starlette()

app.add_middleware(XDownloadOptions)
```
For more detail on X-Download-Options header go to this [NWebsec Site](https://www.nwebsec.com/HttpHeaders/SecurityHeaders/XDownloadOptions)

#### X-Frame

XFrame class sets the X-Frame-Options header

```python
from fastapi import FastAPI
from Secweb.XFrameOptions import XFrame

app = FastAPI()

app.add_middleware(XFrame, Option={'X-Frame-Options': 'DENY'})

# OR

from starlette.applications import Starlette
from Secweb.XFrameOptions import XFrame

app = Starlette()

app.add_middleware(XFrame, Option={'X-Frame-Options': 'DENY'})
```
For more detail on X-Frame-Options header go to this [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)

#### X-Permitted-Cross-Domain-Policies

XPermittedCrossDomainPolicies class sets the X-Permitted-Cross-Domain-Policies header

```python
from fastapi import FastAPI
from Secweb.XPermittedCrossDomainPolicies import XPermittedCrossDomainPolicies

app = FastAPI()

app.add_middleware(XPermittedCrossDomainPolicies, Option={'X-Permitted-Cross-Domain-Policies': 'none'})

# OR

from starlette.applications import Starlette
from Secweb.XPermittedCrossDomainPolicies import XPermittedCrossDomainPolicies

app = Starlette()

app.add_middleware(XPermittedCrossDomainPolicies, Option={'X-Permitted-Cross-Domain-Policies': 'none'})
```
For more detail on X-Permitted-Cross-Domain-Policies header go to this [OWASP Site](https://owasp.org/www-project-secure-headers/#x-permitted-cross-domain-policies)

#### X-XSS-Protection

xXSSProtection class sets the X-XSS-Protection header

```python
from fastapi import FastAPI
from Secweb.xXSSProtection import xXSSProtection

app = FastAPI()

app.add_middleware(xXSSProtection, Option={'X-XSS-Protection': '0'})

# OR

from starlette.applications import Starlette
from Secweb.xXSSProtection import xXSSProtection

app = Starlette()

app.add_middleware(xXSSProtection, Option={'X-XSS-Protection': '0'})
```
For more detail on X-XSS-Protection header go to this [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection)

#### Permissions Policy

PermissionsPolicy class sets the Permissions Policy header

You have to call the PermissionsPolicy class explicitly by providing the Option dictionary it does not have a default value

```python
from fastapi import FastAPI
from Secweb.PermissionsPolicy import PermissionsPolicy

app = FastAPI()

app.add_middleware(PermissionsPolicy, Option={'accelerometer': ['self', '"https://example.com/"'], 'camera': [], 'display-capture': [], 'document-domain': ['self']'})

# OR

from starlette.applications import Starlette
from Secweb.PermissionsPolicy import PermissionsPolicy

app = Starlette()

app.add_middleware(PermissionsPolicy, Option={'accelerometer': ['self', '"https://example.com/"'], 'camera': [], 'display-capture': [], 'document-domain': ['self']'})
```
For more detail on Permissions Policy header go to this [W3C Page](https://www.w3.org/TR/permissions-policy-1/)

## Contributing
Please open an issue or Pull Request (PR) for any Errors/issues in this dev version.

Please make sure to update tests as appropriate.

[Github](https://github.com/tmotagam/Secweb)

## License
[MLP 2.0](https://www.mozilla.org/en-US/MPL/2.0/)