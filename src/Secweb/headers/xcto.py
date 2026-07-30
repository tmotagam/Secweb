from __future__ import annotations
from typing import TYPE_CHECKING

from ..middleware import SetMiddleware

if TYPE_CHECKING:
    from starlette.applications import Starlette

def X_Content_Type_Options(app: Starlette | None = None) -> tuple[bytes, bytes]:
    """
    Sets the `X-Content-Type-Options` HTTP response header.

    The `X-Content-Type-Options` header is a marker used by the server to indicate that the MIME types 
    advertised in the `Content-Type` headers should not be changed and be followed. This is a way to opt 
    out of MIME type sniffing, preventing browsers from executing a malicious script pretending to be 
    an image, for example.

    Args:
        app (Starlette | None, optional): An optional Starlette application instance. 
            If provided, the `X-Content-Type-Options: nosniff` header is injected into the application via middleware. Defaults to None.

    Returns:
        tuple[bytes, bytes]: A tuple representing the header key and its computed value, 
            which is always `(b"X-Content-Type-Options", b"nosniff")`.

    Example:
        >>> X_Content_Type_Options(app)
        (b'X-Content-Type-Options', b'nosniff')
    """
    if app is not None:
        app.add_middleware(SetMiddleware, headers=[(b'X-Content-Type-Options', b'nosniff')])
    return (b'X-Content-Type-Options', b'nosniff')
