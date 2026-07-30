from __future__ import annotations
from typing import TYPE_CHECKING

from ..middleware import SetMiddleware

if TYPE_CHECKING:
    from starlette.applications import Starlette


def X_XSS_Protection(app: Starlette | None = None) -> tuple[bytes, bytes]:
    """
    Sets the `X-XSS-Protection` HTTP response header.

    The `X-XSS-Protection` header is a feature of Internet Explorer, Chrome, and Safari that stops pages 
    from loading when they detect reflected cross-site scripting (XSS) attacks.
    Note: Modern browsers generally rely on Content-Security-Policy instead, and typically setting this to '0' 
    is recommended to avoid cross-site leaks or other vulnerabilities introduced by the XSS auditor.

    Args:
        app (Starlette | None, optional): An optional Starlette application instance. 
            If provided, the `X-XSS-Protection: 0` header is injected into the application via middleware. Defaults to None.

    Returns:
        tuple[bytes, bytes]: A tuple representing the header key and its computed value, 
            which is always `(b"X-XSS-Protection", b"0")`.

    Example:
        >>> X_XSS_Protection(app)
        (b'X-XSS-Protection', b'0')
    """
    if app is not None:
        app.add_middleware(SetMiddleware, headers=[(b'X-XSS-Protection', b'0')])
    return (b'X-XSS-Protection', b'0')
