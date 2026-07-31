<p  align = "center"><img  alt="Secweb logo"  src="https://raw.githubusercontent.com/tmotagam/Secweb/main/Secweb.jpg"></p>
<p  align="center"><em>Secweb helps in setting security headers for FastApi and Starlette</em></p>

---
Secweb is the pack of security headers for fastapi and can also be used for any framework created on starlette. It has 16 security headers for your websites/APIs.


> [!NOTE]
> The Permissions_Policy header lies in [development branch](https://github.com/tmotagam/Secweb/tree/Secweb-Beta#readme)

## **Features**

- 🔒 **Secure Headers**: Automatically apply headers like `Strict-Transport-Security`, `Content-Security-Policy`, and more.

- 🛠️ **Customizable Policies**: Flexibly build your own security policies.

- 🚀 **No External Dependencies**: Lightweight and easy to include in any project that uses **FastAPI** and **Starlette**.

- 🧩 **Easy to Use**: Integrate security headers in just a few lines of code.

- 📚 **Attribution to Trusted Sources**: Implements recommendations from MDN and OWASP.


The list of headers is as follows:

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

15. Clear-Site-Data (decorator)
<br>

16. Cache-Control
<br>

# Requirements

* [Python >= 3.10](https://www.python.org/downloads/)
* [Starlette](https://pypi.org/project/starlette/)

# Installation

```bash
pip install Secweb
```

# Usage

The package Secweb can be used in two different ways:

1. Use the SecWeb class -- it includes all the 15 headers together
<br>

2. Use the 15 header functions separately

## SecWeb class

```Python
from Secweb import SecWeb

SecWeb(app=app) # The app is the ASGIapp required by the Starlette/FastApi to give access to the different methods to the class
```

The above example uses all the default headers value that are preset. You can change the values by creating the `options` dict.

You can also set flags for nonces generation for csp header using the `script_nonce=True` and `style_nonce=True` flags. The `csp_report_only` and `coep_report_only` flags are added for csp and coep report only headers.

```Python
from Secweb import SecWeb

SecWeb(app=app, options={'referrer': ['no-referrer']}, script_nonce=False, style_nonce=False, csp_report_only=False, coep_report_only=False)
```

The `options`-parameter uses 15 keys for calling functions to set the user-defined policies or deactivating headers.

**Note: Deactivating the header(s) can only be done in SecWeb class in options param**

```Python
from Secweb import SecWeb

Secweb(app=app, options={'referrer': False, 'xframe': False})
```

The values are as follows:

1. `'csp'` for calling Content_Security_Policy function to set the user-defined values or deactivate the header
<br>

2. `'referrer'` for calling Referrer_Policy function to set the user-defined values or deactivate the header
<br>

3. `'xdns'` for calling X_DNS_Prefetch_Control function to set the user-defined values or deactivate the header
<br>

4. `'xcdp'` for calling X_Permitted_Cross_Domain_Policies function to set the user-defined values or deactivate the header
<br>

5. `'hsts'` for calling HSTS function to set the user-defined values or deactivate the header
<br>

6. `'wshsts'` for calling WsHSTS function to set the user-defined values for Websockets or deactivate the header
<br>

7. `'xframe'` for calling X_Frame function to set the user-defined values or deactivate the header
<br>

8. `'coep'` for calling Cross_Origin_Embedder_Policy function to set the user-defined values or deactivate the header
<br>

9. `'coop'` for calling Cross_Origin_Opener_Policy function to set the user-defined values or deactivate the header
<br>

10. `'corp'` for calling Cross_Origin_Resource_Policy function to set the user-defined values or deactivate the header
<br>

11. `'cache_control'` for calling Cache_Control function to set the user-defined values or deactivate the header
<br>

12. `'xcto'` for deactivating X-Content-Type-Options header
<br>

13. `'xdo'` for deactivating X-Download-Options header
<br>

14. `'xss'` for deactivating x-xss-protection header
<br>

15. `'oac'` for deactivating Origin-Agent-Cluster header

```python
# Example of all values

SecWeb(app=app, options={'csp': {'default-src': ["'self'"]}, 'xframe':'SAMEORIGIN', 'hsts': {'max-age': 4, 'preload': True}, 'wshsts': {'max-age': 10, 'preload': True},'xcdp': 'all', 'xdns': 'on', 'referrer': ['no-referrer'], 'coep':{'require-corp': True}, 'coop':'same-origin-allow-popups', 'corp': 'same-site', 'cache_control': {'public': True, 's-maxage': 600}, 'xss': False})
```

## Header Functions

### Content Security Policy (CSP)

#### Nonce Processor

The Nonce_Processor module generates script and style nonce tuple for csp header

```python
    # Some code
    style_nonce, script_nonce = Nonce_Processor(ENTROPY=90) # inject the nonce variables into the jinja or html
    # Some more code
```

`ENTROPY` is used to set the nonce length.

The nonce processor needs to be called on the route the following example is of FastApi calling the nonce processor on the route

```python

from fastapi import FastAPI
from Secweb import Nonce_Processor

app = FastAPI()

@app.get("/")
async def root():
    # some code
    style_nonce, script_nonce = Nonce_Processor(ENTROPY=90) # inject the nonce variables into the jinja or html
    # some more code
```
Content_Security_Policy function sets the csp header.

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb import Content_Security_Policy

app = FastAPI()  

Content_Security_Policy(app=app, options={'default-src': ["'self'"], 'base-uri': ["'self'"], 'block-all-mixed-content': []}, script_nonce=False, style_nonce=False, report_only=False)
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb import Content_Security_Policy

routes=[...]

app = Starlette(routes=routes)

Content_Security_Policy(app=app, options={'default-src': ["'self'"], 'base-uri': ["'self'"], 'block-all-mixed-content': []}, script_nonce=False, style_nonce=False, report_only=False)
```

* `script_nonce=False`: nonce flag for inline Javascript
* `style_nonce=False`: nonce flag for inline css
* `report_only=False`: report only flag which activates csp report only header

For more detail on CSP header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy).

For more detail on CSP report only header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy-Report-Only).

### Origin Agent Cluster

Origin_Agent_Cluster function sets the Origin-Agent-Cluster header. It takes no parameters.

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb import Origin_Agent_Cluster

app = FastAPI()
Origin_Agent_Cluster(app)
```
  
#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb import Origin_Agent_Cluster

routes=[...]

app = Starlette(routes=routes)

Origin_Agent_Cluster(app)
```

For more detail on Origin-Agent-Cluster header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Origin-Agent-Cluster).

### Referrer Policy

Referrer_Policy function sets the Referrer-Policy header

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb import Referrer_Policy

app = FastAPI()

Referrer_Policy(app=app, option=['strict-origin-when-cross-origin'])
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb import Referrer_Policy

routes=[...]

app = Starlette(routes=routes)
Referrer_Policy(app=app, option=['strict-origin-when-cross-origin'])
```

For more detail on Referrer-Policy header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy).

### HTTP Strict Transport Security (HSTS)

HSTS function sets the Strict-Transport-Security header

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb import HSTS

app = FastAPI()

HSTS(app=app, options={'max-age': 4, 'preload': True})
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb import HSTS

routes=[...]

app = Starlette(routes=routes)

HSTS(app=app, options={'max-age': 4, 'preload': True})
```

For more detail on Strict-Transport-Security header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security).

### HTTP Strict Transport Security (HSTS) for WebSockets

WsHSTS function sets the Strict-Transport-Security header for Websockets

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb import WsHSTS

app = FastAPI()

WsHSTS(app=app, options={'max-age': 4, 'preload': True})
```
  
#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb import WsHSTS

routes=[...]

app = Starlette(routes=routes)

WsHSTS(app=app, options={'max-age': 4, 'preload': True})
```

For more detail on Strict-Transport-Security header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security).

### X-Content-Type-Options

X_Content_Type_Options function sets the X-Content-Type-Options header the function takes no parameters

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb import X_Content_Type_Options

app = FastAPI()

X_Content_Type_Options(app=app)
```
  
#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb import X_Content_Type_Options

routes=[...]

app = Starlette(routes=routes)

X_Content_Type_Options(app=app)
```

For more detail on X-Content-Type-Options header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options).

### X-DNS-Prefetch-Control

X_DNS_Prefetch_Control function sets the X-DNS-Prefetch-Control header

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb import X_DNS_Prefetch_Control

app = FastAPI()

X_DNS_Prefetch_Control(app=app, option='on')
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb import X_DNS_Prefetch_Control

routes=[...]

app = Starlette(routes=routes)

X_DNS_Prefetch_Control(app=app, option='off')
```

For more detail on X-DNS-Prefetch-Control header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-DNS-Prefetch-Control).

### X-Download-Options

X_Download_Options function sets the X-Download-Options header the function takes no parameter

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb import X_Download_Options

app = FastAPI()

X_Download_Options(app=app)
```

#### For Starlette server
  
```python
from starlette.applications import Starlette
from Secweb import X_Download_Options

routes=[...]

app = Starlette(routes=routes)

X_Download_Options(app=app)
```

For more detail on X-Download-Options header go to [http.dev site](https://http.dev/x-download-options).

### X-Frame

X_Frame function sets the X-Frame-Options header

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb import X_Frame

app = FastAPI()

X_Frame(app=app, option='DENY')
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb import X_Frame

routes=[...]

app = Starlette(routes=routes)

X_Frame(app=app, option='DENY')
```

For more detail on X-Frame-Options header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options).

### X-Permitted-Cross-Domain-Policies

X_Permitted_Cross_Domain_Policies function sets the X-Permitted-Cross-Domain-Policies header

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb import X_Permitted_Cross_Domain_Policies

app = FastAPI()

X_Permitted_Cross_Domain_Policies(app=app, option='none')
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb import X_Permitted_Cross_Domain_Policies

routes=[...]

app = Starlette(routes=routes)

X_Permitted_Cross_Domain_Policies(app=app, option='none')
```

For more detail on X-Permitted-Cross-Domain-Policies header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Permitted-Cross-Domain-Policies).

### X-XSS-Protection

X_XSS_Protection function sets the X-XSS-Protection header the function takes no parameter

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb import X_XSS_Protection

app = FastAPI()

X_XSS_Protection(app=app)
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb import X_XSS_Protection

routes=[...]

app = Starlette(routes=routes)

X_XSS_Protection(app=app)
```

For more detail on X-XSS-Protection header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection).

### Cross Origin Embedder Policy

Cross_Origin_Embedder_Policy function sets the Cross Origin Embedder Policy header

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb import Cross_Origin_Embedder_Policy

app = FastAPI()

Cross_Origin_Embedder_Policy(app=app, option={'unsafe-none': True})
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb import Cross_Origin_Embedder_Policy

routes=[...]

app = Starlette(routes=routes)

Cross_Origin_Embedder_Policy(app=app, option={'unsafe-none': True})
```

* `report_only=False`: report only flag which activates coep report only header

For more detail on Cross Origin Embedder Policy header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy).

For more detail on Cross Origin Embedder Policy report only header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy-Report-Only)

### Cross Origin Opener Policy

Cross_Origin_Opener_Policy function sets the Cross Origin Opener Policy header

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb import Cross_Origin_Opener_Policy

app = FastAPI()

Cross_Origin_Opener_Policy(app=app, option='unsafe-none')
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb import Cross_Origin_Opener_Policy

routes=[...]

app = Starlette(routes=routes)

Cross_Origin_Opener_Policy(app=app, option='unsafe-none')
```

For more detail on Cross Origin Opener Policy header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy).

### Cross Origin Resource Policy

Cross_Origin_Resource_Policy function sets the Cross Origin Resource Policy header

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb import Cross_Origin_Resource_Policy

app = FastAPI()

Cross_Origin_Resource_Policy(app=app, option='same-site')
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb import Cross_Origin_Resource_Policy

routes=[...]

app = Starlette(routes=routes)

Cross_Origin_Resource_Policy(app=app, option='same-site')
```

For more detail on Cross Origin Resource Policy header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Resource-Policy).

### Clear Site Data

Clear_Site_Data decorator sets the Clear-Site-Data header.

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb import Clear_Site_Data

app = FastAPI()

@app.get('/logout')
@Clear_Site_Data(options={'cookies': True, 'storage': True})
async def logout():
    return {"message": "Logged out successfully"}
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb import Clear_Site_Data

@Clear_Site_Data(options={'cookies': True, 'storage': True})
async def logout():
    return {"message": "Logged out successfully"}

routes=[...]

app = Starlette(routes=routes)
```

For more detail on Clear Site Data Header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Clear-Site-Data).

### Cache Control

Cache_Control function sets the Cache-Control header. This is useful for controlling cached data on user`s browser

#### For FastApi server

```python
from fastapi import FastAPI
from Secweb import Cache_Control

app = FastAPI()

Cache_Control(app=app, options={'s-maxage': 600, 'public': True})
```

#### For Starlette server

```python
from starlette.applications import Starlette
from Secweb import Cache_Control

routes=[...]

app = Starlette(routes=routes)

Cache_Control(app=app, options={'s-maxage': 600, 'public': True})
```

For more detail on Cache Control Header go to [MDN Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control).

# Contributing

Pull requests and Issues are welcome. For major changes, please open an issue first to discuss what you would like to change.

**[Github](https://github.com/tmotagam/Secweb)**

# License

**[MLP 2.0](https://www.mozilla.org/en-US/MPL/2.0/)**

# Secweb Icon

**[Secweb Icon](https://github.com/tmotagam/Secweb/blob/main/Secweb.jpg) © 2021 - 2026 by [Motagamwala Taha Arif Ali](https://github.com/tmotagam) is licensed under [Attribution-NonCommercial-NoDerivatives 4.0 International](https://creativecommons.org/licenses/by-nc-nd/4.0/?ref=chooser-v1)**
