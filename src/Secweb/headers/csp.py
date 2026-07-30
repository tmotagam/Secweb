from __future__ import annotations
from typing import TYPE_CHECKING
from secrets import token_urlsafe
from warnings import warn

from ..middleware import SetMiddleware

if TYPE_CHECKING:
    from .._types import Content_Security_Policy_Options
    from typing import Callable
    from starlette.applications import Starlette

style_nonce: str | None = None
script_nonce: str | None = None

def Nonce_Processor(ENTROPY: int = 90) -> tuple[str, str]:
    """
    Generates cryptographically secure nonces for Content Security Policy.

    This function sets `style_nonce` and `script_nonce` using Python's 
    `secrets.token_urlsafe` to ensure they are unique and unpredictable for each request lifecycle.

    Args:
        ENTROPY (int, optional): The number of bytes of randomness to use for the nonce. 
            Defaults to 90.

    Returns:
        tuple[str, str]: A tuple containing the (style_nonce, script_nonce).

    Example:
        >>> Nonce_Processor()
        ('aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890-_', '0987654321ZyXwVuTsRqPoNmLkJiHgFeDcBa_-')
    """
    global style_nonce
    global script_nonce
    style_nonce = token_urlsafe(ENTROPY)
    script_nonce = token_urlsafe(ENTROPY)
    return (style_nonce, script_nonce)

DEFAULT_CSP_OPTIONS: Content_Security_Policy_Options = {
    'default-src': ["'self'"],
    'base-uri': ["'self'"],
    'block-all-mixed-content': [],
    'font-src': ["'self'", 'https:', 'data:'],
    'frame-ancestors': ["'self'"],
    'img-src': ["'self'", 'data:'],
    'object-src': ["'none'"],
    'script-src': ["'self'"],
    'script-src-attr': ["'none'"],
    'style-src': ["'self'", "https:", "'unsafe-inline'"],
    'upgrade-insecure-requests': [],
    'require-trusted-types-for': ["'script'"]
}

VALID_CSP_DIRECTIVES = [
    'child-src', 'connect-src', 'default-src', 'font-src', 'frame-src', 'img-src',
    'manifest-src', 'media-src', 'object-src', 'script-src', 'script-src-elem',
    'script-src-attr', 'style-src', 'style-src-elem', 'style-src-attr', 'worker-src',
    'base-uri', 'sandbox', 'form-action', 'frame-ancestors', 'report-uri', 'report-to',
    'block-all-mixed-content', 'require-trusted-types-for', 'trusted-types',
    'upgrade-insecure-requests', 'fenced-frame-src'
]

def Content_Security_Policy(
    app: Starlette | None = None,
    options: Content_Security_Policy_Options = DEFAULT_CSP_OPTIONS,
    script_nonce_flag: bool = False,
    style_nonce_flag: bool = False,
    report_only: bool = False
) -> tuple[bytes, bytes] | Callable:
    """
    Sets the `Content-Security-Policy` (CSP) HTTP response header.

    CSP is an added layer of security that helps to detect and mitigate certain types of attacks, 
    including Cross-Site Scripting (XSS) and data injection attacks.

    Args:
        app (Starlette | None, optional): An optional Starlette application instance. 
            If provided, the header is injected into the application via middleware. Defaults to None.
        options (Content_Security_Policy_Options, optional): A dictionary mapping CSP directives to lists of source values.
            Defaults to a strict base configuration (`DEFAULT_CSP_OPTIONS`).
        script_nonce_flag (bool, optional): If True, dynamically appends a nonce to the `script-src` directive. Defaults to False.
        style_nonce_flag (bool, optional): If True, dynamically appends a nonce to the `style-src` directive. Defaults to False.
        report_only (bool, optional): If True, sets the `Content-Security-Policy-Report-Only` header instead,
            which reports violations without blocking the resources. Requires 'report-uri' or 'report-to'. Defaults to False.

    Returns:
        tuple[bytes, bytes] | Callable: A tuple representing the header key and its computed value if no nonces are used.
            If `script_nonce_flag` or `style_nonce_flag` is True, returns a callable that generates dynamic headers per request.

    Raises:
        ValueError: If unsupported CSP directives are provided.
        ValueError: If `report_only` is True but reporting endpoints are missing.
        ValueError: If a nonce flag is True but the corresponding directive ('script-src' or 'style-src') is missing.

    Example:
        >>> Content_Security_Policy(app, options={'default-src': ["'self'"], 'script-src': ["'self'", 'https://apis.google.com']})
        (b'Content-Security-Policy', b"default-src 'self'; script-src 'self' https://apis.google.com")
    """
    if set(options.keys()).difference(VALID_CSP_DIRECTIVES):
        invalid_keys = set(options.keys()).difference(VALID_CSP_DIRECTIVES)
        raise ValueError(f"Invalid option(s) for Content-Security-Policy: {', '.join(invalid_keys)}")

    if report_only:
        if 'report-to' not in options and 'report-uri' not in options:
            raise ValueError('report-to and/or report-uri are compulsory for report_only policy')
        if 'sandbox' in options:
            warn('sandbox option is not supported in report-only policy', SyntaxWarning, stacklevel=2)

    if script_nonce_flag and 'script-src' not in options:
        raise ValueError('script-src is compulsory for nonce')

    if style_nonce_flag and 'style-src' not in options:
        raise ValueError('style-src is compulsory for nonce')

    header_name = b'Content-Security-Policy-Report-Only' if report_only else b'Content-Security-Policy'

    parts: list[str] = []
    for key, values in options.items():
        if not isinstance(values, list):
            val_list = [str(values)]
        else:
            val_list = [str(v) for v in values]
            
        if key == 'script-src' and script_nonce_flag:
            val_list.append(f"'nonce-{{script_nonce_value}}'")
        if key == 'style-src' and style_nonce_flag:
            val_list.append(f"'nonce-{{style_nonce_value}}'")

        if val_list:
            parts.append(f"{key} {' '.join(val_list)}")
        else:
            parts.append(key)

    policy_template = "; ".join(parts)

    if script_nonce_flag or style_nonce_flag:
        def generate_dynamic_csp():
            import Secweb.headers.csp as csp_module
            kwargs = {}
            if script_nonce_flag:
                kwargs["script_nonce_value"] = csp_module.script_nonce
            if style_nonce_flag:
                kwargs["style_nonce_value"] = csp_module.style_nonce
            return (header_name, policy_template.format(**kwargs).encode('latin-1'))
        
        if app is not None:
            app.add_middleware(SetMiddleware, headers=[], dynamic_headers=[generate_dynamic_csp])
        return generate_dynamic_csp

    policy_bytes = policy_template.encode('latin-1')

    if app is not None:
        app.add_middleware(SetMiddleware, headers=[(header_name, policy_bytes)])

    return (header_name, policy_bytes)
