from __future__ import annotations
from typing import TYPE_CHECKING

from ..middleware import SetMiddleware

if TYPE_CHECKING:
    from starlette.applications import Starlette

def X_Download_Options(app: Starlette | None = None) -> tuple[bytes, bytes]:
    """
    Sets the `X-Download-Options` HTTP response header.

    The `X-Download-Options` header is specific to Internet Explorer 8 and later. It prevents 
    the browser from rendering downloaded files within the browser context. By setting it to 'noopen',
    users are prevented from opening malicious HTML files that might execute script in the site's context.

    Args:
        app (Starlette | None, optional): An optional Starlette application instance. 
            If provided, the `X-Download-Options: noopen` header is injected into the application via middleware. Defaults to None.

    Returns:
        tuple[bytes, bytes]: A tuple representing the header key and its computed value, 
            which is always `(b"X-Download-Options", b"noopen")`.

    Example:
        >>> X_Download_Options(app)
        (b'X-Download-Options', b'noopen')
    """
    if app is not None:
        app.add_middleware(SetMiddleware, headers=[(b'X-Download-Options', b'noopen')])
    return (b'X-Download-Options', b'noopen')
