from __future__ import annotations
from typing import TYPE_CHECKING

from ..middleware import SetMiddleware

if TYPE_CHECKING:
    from starlette.applications import Starlette
    from .._types import HSTS_Options


def HSTS(app: Starlette | None = None, options: HSTS_Options = {'max-age': 31536000, 'includeSubDomains': True, 'preload': False }) -> tuple[bytes, bytes]:
    """
    Sets the `Strict-Transport-Security` (HSTS) HTTP response header.

    The HSTS header lets a web site tell browsers that it should only be accessed using HTTPS, 
    instead of using HTTP.

    Args:
        app (Starlette | None, optional): An optional Starlette application instance. 
            If provided, the header is injected into the application via middleware. Defaults to None.
        options (HSTS_Options, optional): A dictionary of HSTS directives.
            `max-age` (int) is required. `includeSubDomains` (bool) and `preload` (bool) are optional.
            Defaults to {'max-age': 31536000, 'includeSubDomains': True, 'preload': False}.

    Returns:
        tuple[bytes, bytes]: A tuple representing the header key and its computed value, 
            e.g., `(b"Strict-Transport-Security", b"max-age=31536000; includeSubDomains")`.

    Raises:
        ValueError: If an unsupported directive is provided, if `max-age` is missing, or if a value is invalid.

    Example:
        >>> HSTS(app, options={'max-age': 31536000, 'includeSubDomains': True})
        (b'Strict-Transport-Security', b'max-age=31536000; includeSubDomains')
    """
    if set(options).difference(['max-age', 'includeSubDomains', 'preload']) or 'max-age' not in options:
        raise ValueError('Invalid option(s) for HSTS (Must be one or more of: max-age (compulsory), includeSubDomains, preload)')
    header_value: list[bytes] = []
    for key, value in options.items():
        if isinstance(value, bool):
            if value:
                header_value.append(key.encode('latin-1'))
        elif isinstance(value, int) and value > 0:
            header_value.append(f"{key}={value}".encode('latin-1'))
        else:
            raise ValueError(f'Invalid value for HSTS ({key}={value})')
    if app is not None:
        app.add_middleware(SetMiddleware, headers=[('Strict-Transport-Security'.encode('latin-1'), b'; '.join(header_value))])
    return ('Strict-Transport-Security'.encode('latin-1'), b'; '.join(header_value))


def WsHSTS(app: Starlette | None = None, options: HSTS_Options = {'max-age': 31536000, 'includeSubDomains': True, 'preload': False }) -> tuple[bytes, bytes]:
    """
    Sets the `Strict-Transport-Security` (HSTS) header specifically for WebSocket connections.

    This behaves identically to `HSTS()` but configures the middleware to apply the HSTS header 
    to WebSocket upgrade requests in the Starlette application.

    Args:
        app (Starlette | None, optional): An optional Starlette application instance. 
            If provided, the header is injected via WebSocket middleware. Defaults to None.
        options (HSTS_Options, optional): A dictionary of HSTS directives.
            `max-age` (int) is required. `includeSubDomains` (bool) and `preload` (bool) are optional.
            Defaults to {'max-age': 31536000, 'includeSubDomains': True, 'preload': False}.

    Returns:
        tuple[bytes, bytes]: A tuple representing the header key and its computed value.

    Raises:
        ValueError: If an unsupported directive is provided, if `max-age` is missing, or if a value is invalid.

    Example:
        >>> WsHSTS(app, options={'max-age': 86400})
        (b'Strict-Transport-Security', b'max-age=86400')
    """
    if set(options).difference(['max-age', 'includeSubDomains', 'preload']) or 'max-age' not in options:
        raise ValueError('Invalid option(s) for WsHSTS (Must be one or more of: max-age (compulsory), includeSubDomains, preload)')
    header_value: list[bytes] = []
    for key, value in options.items():
        if isinstance(value, bool):
            if value:
                header_value.append(key.encode('latin-1'))
        elif isinstance(value, int) and value > 0:
            header_value.append(f"{key}={value}".encode('latin-1'))
        else:
            raise ValueError(f'Invalid value for WsHSTS ({key}={value})')
    if app is not None:
        app.add_middleware(SetMiddleware, headers=[], wshsts=('Strict-Transport-Security'.encode('latin-1'), b'; '.join(header_value)))
    return ('Strict-Transport-Security'.encode('latin-1'), b'; '.join(header_value))
