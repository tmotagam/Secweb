# Secweb 2.0.0 — Release Notes

**Release Date:** 30 July 2026  
**Python Requirement:** >= 3.10  
**License:** MPL-2.0  
**PyPI:** [Secweb](https://pypi.org/project/Secweb/)  
**GitHub:** [tmotagam/Secweb](https://github.com/tmotagam/Secweb)

---

> [!IMPORTANT]
> **Secweb 2.0.0 is a major release with breaking changes.** It is not backwards compatible with the 1.x series. Please read the [Migration Guide](#migration-from-1x-to-20) below before upgrading.

## Highlights

Secweb 2.0.0 is a ground-up rewrite of the library, delivering a cleaner API, full type safety, a modern Python baseline, and zero required dependencies. Every header module has been redesigned to work with single middleware so no matter how many headers get activated the response passthrough always one middleware.

---

## ⚡ What's New

### 🏗️ Complete Architecture Rewrite

- **Standalone header functions** — Every header (CSP, HSTS, COEP, COOP, etc.) can now be used independently as a function call, returning `tuple[bytes, bytes]` header pairs or passing it to the middleware if app is passed to the function. You no longer need the `SecWeb` class at all if you want granular control.
- **Optional `app` parameter** — All header functions accept an optional `app: Starlette | None` first argument. Pass your app to auto-inject via middleware, or omit it to get raw header tuples.
- **Smart middleware deduplication** — The new middleware factory detects if your app is already wrapped and extends the existing instance instead of nesting another layer. This eliminates redundant middleware stacking when calling multiple header functions on the same app.
- **Unified `SecWeb` class** — The `SecWeb(app, options={...})` entry point remains the recommended one-liner for applying all headers at once, now with a cleaner `SecWeb_Options` TypedDict interface.

### 🔒 New Headers & Features

| Header / Feature | Description |
|---|---|
| **`Clear-Site-Data`** | New decorator-based header (`@Clear_Site_Data()`) for route-level cache/cookie/storage clearing. Supports `*`, `cache`, `cookies`, `storage`, `prefetchCache`, `prerenderCache`, and `clientHints`. |
| **COEP Report-Only** | `Cross-Origin-Embedder-Policy-Report-Only` mode via `report_only=True` parameter. |
| **COEP `credentialless`** | New `credentialless` policy option for COEP alongside `require-corp` and `unsafe-none`. |
| **COEP `report-to`** | Optional `report-to` endpoint configuration for COEP violation reporting. |
| **COOP `noopener-allow-popups`** | New policy value for Cross-Origin-Opener-Policy. |

### 🏷️ Full Type Safety

- **`py.typed` marker** — Secweb is now a PEP 561 compliant typed package.
- **Comprehensive `TypedDict` definitions** — All options dictionaries (`Content_Security_Policy_Options`, `HSTS_Options`, `Cache_Control_Options`, `Permissions_Policy_Options`, `Clear_Site_Data_Options`, `Cross_Origin_Embedder_Policy_Options`, `SecWeb_Options`) are defined as `TypedDict` in `_types.py`.
- **`Literal` types** — Enum-style options (COOP, CORP, X-Frame, Referrer, etc.) use `Literal` types for IDE autocompletion and static analysis.
- **Full `TYPE_CHECKING` guards** — Type imports are gated behind `if TYPE_CHECKING:` to avoid runtime overhead.

### 🐍 Modern Python

- **Python >= 3.10 required** (up from 3.6-3.9 in 1.x).
- **`from __future__ import annotations`** used throughout for PEP 604 union syntax (`X | Y`).
- **Zero runtime dependencies** — Starlette/FastAPI are only imported under `TYPE_CHECKING`.

### 🛡️ Enhanced Validation

- **Strict option validation** — All header functions validate input keys against an explicit allowlist and raise `ValueError` with more descriptive messages for invalid options.

### 📖 Documentation

- **Comprehensive docstrings** — Every public function and class includes full Google-style docstrings with `Args`, `Returns`, `Raises`, and `Example` sections.

---

## 💥 Breaking Changes

### API Changes

| 1.x | 2.0 | Notes |
|---|---|---|
| `ContentSecurityPolicy(app, Option={...})` | `Content_Security_Policy(app, options={...})` | Renamed parameter from `Option` to `options` |
| `HSTS(app, Option={...})` | `HSTS(app, options={...})` | Same parameter rename |
| Header classes (e.g. `ContentSecurityPolicy`) | Header functions (e.g. `Content_Security_Policy`) | Classes replaced by functions |
| `SecWeb(app=app, Option={...})` | `SecWeb(app, options={...})` | Keyword `Option` → `options`, named `app` → positional |
| Individual header classes as middleware | Headers return `tuple[bytes, bytes]` or callable | No longer middleware classes |

### Python Version

- **Minimum Python version raised from 3.9 → 3.10**

### Import Paths

```python
# 1.x
from Secweb.ContentSecurityPolicy import ContentSecurityPolicy
from Secweb.xXSSProtection import xXSSProtection

# 2.0
from Secweb import SecWeb, Content_Security_Policy, X_XSS_Protection
```

---

## Migration from 1.x to 2.0

### Standalone Header Usage (New in 2.0)

```python
from Secweb import X_XSS_Protection, X_Frame, Content_Security_Policy

# Auto-inject into app via middleware
X_XSS_Protection(app)
X_Frame(app, option='DENY')
Content_Security_Policy(app, options={'default-src': ["'self'"]})

# Or get raw header tuples
header_name, header_value = X_Frame(option='SAMEORIGIN')
```

### Clear-Site-Data Decorator (New in 2.0)

```python
from Secweb import Clear_Site_Data

@app.get("/logout")
@Clear_Site_Data(options={'cookies': True, 'storage': True})
async def logout():
    return {"message": "Logged out"}
```

---

## Full File Listing

| File | Purpose |
|---|---|
| `__init__.py` | Package entry point, re-exports `SecWeb` and all headers |
| `_types.py` | All TypedDict and Literal type definitions |
| `index.py` | `SecWeb` unified class |
| `middleware.py` | `_SetHeadersMiddleware` ASGI middleware and `SetMiddleware` factory |
| `headers/__init__.py` | Header module re-exports |
| `headers/csp.py` | Content-Security-Policy |
| `headers/hsts.py` | Strict-Transport-Security (HTTP & WebSocket) |
| `headers/coep.py` | Cross-Origin-Embedder-Policy |
| `headers/coop.py` | Cross-Origin-Opener-Policy |
| `headers/corp.py` | Cross-Origin-Resource-Policy |
| `headers/cache_control.py` | Cache-Control |
| `headers/clear_site_data.py` | Clear-Site-Data (decorator) |
| `headers/referrer.py` | Referrer-Policy |
| `headers/xframe.py` | X-Frame-Options |
| `headers/xss.py` | X-XSS-Protection |
| `headers/xcto.py` | X-Content-Type-Options |
| `headers/xcdp.py` | X-Permitted-Cross-Domain-Policies |
| `headers/xdns.py` | X-DNS-Prefetch-Control |
| `headers/xdo.py` | X-Download-Options |
| `headers/oac.py` | Origin-Agent-Cluster |
| `py.typed` | PEP 561 typed package marker |

---

## Acknowledgements

Secweb 2.0.0 is authored by **Motagamwala Taha Arif Ali** ([tmotagam](https://github.com/tmotagam)).
