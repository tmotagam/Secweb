# Secweb — Full Changelog

> Complete version history from **1.0.0** to **2.0.0**
>
> **Repository:** [tmotagam/Secweb](https://github.com/tmotagam/Secweb)  
> **PyPI:** [Secweb](https://pypi.org/project/Secweb/)  
> **Author:** Motagamwala Taha Arif Ali

---

## [2.0.0] — July 30, 2026  *(Secweb-Beta / Secweb-Stable)*

> [GitHub Release](https://github.com/tmotagam/Secweb/releases/tag/2.0.0) · Dev wheel: `Secweb_dev-2.0.0`

> [PYPI Release](https://pypi.org/project/Secweb/2.0.0/) · Stable wheel: `Secweb-2.0.0`

> [!CAUTION]
> **Major release — Not backwards compatible with 1.x**

### ⚡ Architecture
- Complete ground-up rewrite of the entire library
- Header classes replaced by standalone functions returning `tuple[bytes, bytes]`
- All header functions accept optional `app: Starlette | None` — pass app to auto-inject via middleware, or omit to get raw header tuples
- New `_SetHeadersMiddleware` ASGI middleware with smart deduplication via `SetMiddleware` factory
- Unified `SecWeb(app, options={...})` class retained as the recommended one-liner entry point

### 🆕 New Headers & Features
- **`Clear-Site-Data`** — New decorator-based header (`@Clear_Site_Data()`) for route-level data clearing; supports `*`, `cache`, `cookies`, `storage`, `prefetchCache`, `prerenderCache`, `clientHints`
- **COEP `credentialless`** policy option
- **COEP `report-to`** endpoint configuration
- **COEP Report-Only** mode (`report_only=True`)
- **COOP `noopener-allow-popups`** policy value
- **Expanded Permissions Policy (*Beta*)** — 45+ features including `aria-notify`, `captured-surface-control`, `ch-ua-high-entropy-values`, `compute-pressure`, `deferred-fetch`, `deferred-fetch-minimal`, `local-network`, `local-network-access`, `loopback-network`, `on-device-speech-recognition`, `private-state-token-issuance`, `private-state-token-redemption`, `summarizer`, and more

### 🏷️ Type Safety
- Added `py.typed` marker (PEP 561 compliant)
- Comprehensive `TypedDict` definitions for all option dictionaries in `_types.py`
- `Literal` types for enum-style options (COOP, CORP, X-Frame, Referrer, etc.)
- All type imports gated behind `if TYPE_CHECKING:` for zero runtime overhead

### 🛡️ Validation
- Strict input validation on all header functions with more descriptive `ValueError` messages

### 📖 Documentation
- Full Google-style docstrings on every public functions and classes

### 💥 Breaking Changes
- **Python >= 3.10 required** (up from 3.6-3.9)
- Header classes replaced by functions (e.g., `ContentSecurityPolicy` → `Content_Security_Policy`)
- `Option` parameter renamed to `options` / `option` across all APIs
- Import paths changed (e.g., `from Secweb.ContentSecurityPolicy import ...` → `from Secweb import ...`)

---

## [1.30.x] — January 15, 2026  *(Secweb-Beta / Secweb-Stable)*

> [GitHub Release](https://github.com/tmotagam/Secweb/releases/tag/1.30.x) · Dev wheel: `Secweb_dev-1.30.12`

> [PYPI Release](https://pypi.org/project/Secweb/1.30.10/) · Stable wheel: `Secweb-1.30.10`

### Changes
- Full types added across the codebase
- Python minimum version upgraded to **3.9**
- New policies added to **Permissions Policy** **(Beta)**
- **`Clear-Site-Data`** header support added
- All changes backwards compatible with 1.x

---

## [1.25.x] — July 14, 2025  *(Secweb-Beta / Secweb-Stable)*

> [GitHub Release](https://github.com/tmotagam/Secweb/releases/tag/1.25.x) · Dev wheel: `Secweb_dev-1.25.7`

> [PYPI Release](https://pypi.org/project/Secweb/1.25.2/) · Stable wheel: `Secweb-1.25.2`

### Changes
- Partial types added
- Python minimum version upgraded to **3.8**
- New policies added to **Permissions Policy** **(Beta)**
- New directives added to **CSP**
- New policy values added to **COOP**
- All changes backwards compatible with 1.x

---

## [1.18.x] — January 15, 2025  *(Secweb-Beta / Secweb-Stable)*

> [GitHub Release](https://github.com/tmotagam/Secweb/releases/tag/1.18.x) · Dev wheel: `Secweb_dev-1.18.5`

> [PYPI Release](https://pypi.org/project/Secweb/1.18.1/) · Stable wheel: `Secweb-1.18.1`

### Changes
- **Option parameter changed** for the following headers:
  - Cross-Origin-Embedder-Policy (COEP)
  - Cross-Origin-Opener-Policy (COOP)
  - Cross-Origin-Resource-Policy (CORP)
  - Policies updated in **Permissions Policy** **(Beta)**
  - Referrer-Policy
  - X-DNS-Prefetch-Control
  - X-Frame-Options
  - X-Permitted-Cross-Domain-Policies
- All changes backwards compatible

---

## [1.11.x] — June 18, 2024  *(Secweb-Beta / Secweb-Stable)*

> [GitHub Release](https://github.com/tmotagam/Secweb/releases/tag/1.11.x) · Dev wheel: `Secweb_dev-1.11.1`

> [PYPI Release](https://pypi.org/project/Secweb/1.11.0/) · Stable wheel: `Secweb-1.11.0`

### Changes
- Policies updated in **Permissions Policy** **(Beta)**
- **CSP Report-Only** header support (`Content-Security-Policy-Report-Only`)
- **Ability to deactivate individual middleware** from the `SecWeb` class by setting header options to `False`
- Sigstore signatures for production and development wheels

---

## [1.9.x] — December 7, 2023  *(Secweb-Beta / Secweb-Stable)*

> [GitHub Release](https://github.com/tmotagam/Secweb/releases/tag/1.9.x) · Dev wheel: `Secweb_dev-1.9.2`

> [PYPI Release](https://pypi.org/project/Secweb/1.9.1/) · Stable wheel: `Secweb-1.9.1`

### Changes
- Sigstore signatures for production and development wheels
- Policies updated in **Permissions Policy** **(Beta)**
- Internal improvements and maintenance

---

## [1.7.x] — June 12–14, 2023  *(Secweb-Beta / Secweb-Stable)*

> [GitHub Release](https://github.com/tmotagam/Secweb/releases/tag/1.7.x) · Dev wheel: `Secweb_dev-1.7.3`

> [PYPI Release](https://pypi.org/project/Secweb/1.7.2/) · Stable wheel: `Secweb-1.7.2`

### Changes
- **Without-types release** (1.7.3 and 1.7.2) — release without type annotations for broader compatibility
- Sigstore cosign signatures for both dev and production Secweb wheels
- Policies updated in **Permissions Policy** **(Beta)**

---

## [1.6.0] — 2022  *(PyPI Stable)*

> [PyPI](https://pypi.org/project/Secweb/1.6.0/) · Python >= 3.7

### Changes
- Added **Permission Policy** header support **(Beta)**
- Added **WebSocket HSTS** support
- General stability improvements
- Previous beta releases consolidated under `previous-beta-releases` tag on GitHub

---

## [1.5.1] — 2022  *(PyPI Stable)*

> [PyPI](https://pypi.org/project/Secweb/1.5.1/) · Python >= 3.7

### Changes
- Python minimum version raised from **3.6** to **3.7**
- Bug fixes and stability improvements
- Added **`Nonce_Processor`** for CSP script/style nonces
- Internal middleware improvements

---

## [1.3.0] — 2021  *(PyPI Stable)*

> [PyPI](https://pypi.org/project/Secweb/1.3.0/) · Python >= 3.6

### Changes
- Added **CSP nonce support** (`script_nonce`, `style_nonce` parameters)
- Added **Origin-Agent-Cluster** header
- Added **X-Permitted-Cross-Domain-Policies** header
- Expanded CSP directives support
- Internal code refactoring

---

## [1.0.0] — 2021  *(PyPI Stable — Initial Release)*

> [PyPI](https://pypi.org/project/Secweb/1.0.0/) · Python >= 3.6

### Features (Initial Release)
- **`SecWeb`** — Unified class to apply all security headers at once via middleware
- **Content-Security-Policy (CSP)** — Full directive support with default strict policy
- **Strict-Transport-Security (HSTS)** — Configurable `max-age`, `includeSubDomains`, `preload`
- **Cross-Origin-Embedder-Policy (COEP)** — `require-corp` and `unsafe-none`
- **Cross-Origin-Opener-Policy (COOP)** — `same-origin`, `same-origin-allow-popups`, `unsafe-none`
- **Cross-Origin-Resource-Policy (CORP)** — `same-origin`, `same-site`, `cross-origin`
- **X-XSS-Protection** — XSS filter header
- **X-Frame-Options** — `SAMEORIGIN`, `DENY`
- **X-Content-Type-Options** — `nosniff`
- **X-DNS-Prefetch-Control** — `on`, `off`
- **X-Download-Options** — `noopen`
- **Referrer-Policy** — Multiple policy values support
- Starlette and FastAPI compatible
- Middleware-based architecture

---

## Summary of Evolution

| Version | Key Milestone |
|---|---|
| **1.0.0** | Initial release — 12 security headers, middleware architecture |
| **1.3.0** | CSP nonces, Origin-Agent-Cluster, X-Permitted-Cross-Domain-Policies |
| **1.5.1** | Python 3.7+, Nonce_Processor, stability fixes |
| **1.6.0** | Added Permissions-Policy, WebSocket HSTS |
| **1.7.x** | Sigstore signatures for dev, dev wheel with Permissions Policy |
| **1.9.x** | Sigstore signatures for prod + dev |
| **1.11.x** | CSP Report-Only, middleware deactivation |
| **1.18.x** | Option parameter redesign for 7 headers |
| **1.25.x** | Partial types, Python 3.8+, new CSP/COOP/Permissions policies |
| **1.30.x** | Full types, Python 3.9+, Clear-Site-Data, new Permissions policies |
| **2.0.0** | **Complete rewrite** — standalone functions, full TypedDict types, Python 3.10+, Cache-Control, Clear-Site-Data decorator, COEP report-only, smart middleware dedup |
