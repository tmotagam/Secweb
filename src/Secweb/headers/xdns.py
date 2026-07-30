from __future__ import annotations
from typing import TYPE_CHECKING

from ..middleware import SetMiddleware

if TYPE_CHECKING:
    from starlette.applications import Starlette
    from .._types import X_DNS_Prefetch_Control_Options

def X_DNS_Prefetch_Control(app: Starlette | None = None, option: X_DNS_Prefetch_Control_Options = 'off') -> tuple[bytes, bytes]:
    """
    Sets the `X-DNS-Prefetch-Control` HTTP response header.

    The `X-DNS-Prefetch-Control` header controls DNS prefetching, a feature by which browsers proactively 
    perform domain name resolution on both links that the user may choose to follow as well as URLs 
    for items referenced by the document, including images, CSS, JavaScript, and so forth.

    Args:
        app (Starlette | None, optional): An optional Starlette application instance. 
            If provided, the header is injected into the application via middleware. Defaults to None.
        option (X_DNS_Prefetch_Control_Options, optional): The policy directive to apply.
            Valid values are: "on" or "off". Defaults to 'off'.

    Returns:
        tuple[bytes, bytes]: A tuple representing the header key and its computed value, 
            e.g., `(b"X-DNS-Prefetch-Control", b"off")`.

    Raises:
        ValueError: If an unsupported policy directive is provided.

    Example:
        >>> X_DNS_Prefetch_Control(app, option="off")
        (b'X-DNS-Prefetch-Control', b'off')
    """
    if option not in ('off', 'on'):
        raise ValueError('Invalid option for X-DNS-Prefetch-Control (must be "off" or "on")')
    if app is not None:
        app.add_middleware(SetMiddleware, headers=[(b'X-DNS-Prefetch-Control', option.encode('latin-1'))])
    return (b'X-DNS-Prefetch-Control', option.encode('latin-1'))
