from __future__ import annotations
from typing import TYPE_CHECKING

from ..middleware import SetMiddleware

if TYPE_CHECKING:
    from .._types import Cache_Control_Options
    from starlette.applications import Starlette

def Cache_Control(app: Starlette | None = None, options: Cache_Control_Options = {'max-age': 604800, 'private': True }) -> tuple[bytes, bytes]:
    """
    Sets the `Cache-Control` HTTP response header.

    The `Cache-Control` HTTP header holds directives (instructions) for caching in both requests and responses. 
    It controls how, and for how long, the browser and other intermediate caches can cache the response.

    This function configures the caching behavior by either adding a middleware to a given Starlette app
    or returning a tuple of header bytes.
    
    Args:
        app (Starlette | None, optional): An optional Starlette application instance. 
            If provided, the caching header is injected into the application via middleware. Defaults to None.
        options (Cache_Control_Options, optional): A dictionary of cache directives.
            Valid boolean directives: 'no-cache', 'no-store', 'no-transform', 'must-revalidate', 
            'proxy-revalidate', 'must-understand', 'private', 'public', 'immutable'.
            Valid integer directives (in seconds): 'max-age', 's-maxage', 'stale-while-revalidate', 'stale-if-error'.
            Defaults to {'max-age': 604800, 'private': True}.

    Returns:
        tuple[bytes, bytes]: A tuple representing the header key and its computed value, 
            e.g., `(b"Cache-Control", b"max-age=604800, private")`.

    Raises:
        ValueError: If an unsupported directive is provided in `options`.
        ValueError: If a directive's value type is neither `bool` nor `int`.
    
    Example:
        >>> Cache_Control(app, options={'public': True, 'max-age': 3600})
        (b'Cache-Control', b'max-age=3600, public')
    """
    if set(options).difference(['max-age', 's-maxage', 'no-cache', 'no-store', 'no-transform', 'must-revalidate', 'proxy-revalidate', 'must-understand', 'private', 'public', 'immutable', 'stale-while-revalidate', 'stale-if-error']):
        raise ValueError('Invalid option(s) for Cache-Control (Must be one or more of: max-age, s-maxage, no-cache, no-store, no-transform, must-revalidate, proxy-revalidate, must-understand, private, public, immutable, stale-while-revalidate, stale-if-error)')
    header_value: list[bytes] = []
    for key, value in options.items():
        if isinstance(value, bool):
            if value:
                header_value.append(key.encode('latin-1'))
        elif isinstance(value, int):
            header_value.append(f"{key}={value}".encode('latin-1'))
        else:
            raise ValueError(f'Invalid value for Cache-Control ({key}={value})')
    if app is not None:
        app.add_middleware(SetMiddleware, headers=[(b"Cache-Control", b", ".join(header_value))])
    return (b"Cache-Control", b", ".join(header_value))
        
