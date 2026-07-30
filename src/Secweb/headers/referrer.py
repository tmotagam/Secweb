from __future__ import annotations
from typing import TYPE_CHECKING

from ..middleware import SetMiddleware

if TYPE_CHECKING:
    from .._types import Referrer_Policy_Options
    from starlette.applications import Starlette

def Referrer_Policy(app: Starlette | None = None, option: Referrer_Policy_Options = ['strict-origin-when-cross-origin']) -> tuple[bytes, bytes]:
    """
    Sets the `Referrer-Policy` HTTP response header.

    The `Referrer-Policy` header controls how much referrer information (sent via the `Referer` header) 
    should be included with requests made from a document.

    Args:
        app (Starlette | None, optional): An optional Starlette application instance. 
            If provided, the header is injected into the application via middleware. Defaults to None.
        option (Referrer_Policy_Options, optional): A list of one or more fallback policy directives.
            Valid values are: 'no-referrer', 'no-referrer-when-downgrade', 'origin', 
            'origin-when-cross-origin', 'same-origin', 'strict-origin', 'strict-origin-when-cross-origin', 
            and 'unsafe-url'. Defaults to ['strict-origin-when-cross-origin'].

    Returns:
        tuple[bytes, bytes]: A tuple representing the header key and its computed value, 
            e.g., `(b"Referrer-Policy", b"strict-origin-when-cross-origin")`.

    Raises:
        ValueError: If an unsupported policy directive is provided.

    Example:
        >>> Referrer_Policy(app, option=["no-referrer", "strict-origin-when-cross-origin"])
        (b'Referrer-Policy', b'no-referrer, strict-origin-when-cross-origin')
    """
    if set(option).difference([
        'no-referrer',
        'no-referrer-when-downgrade',
        'origin',
        'origin-when-cross-origin',
        'same-origin',
        'strict-origin',
        'strict-origin-when-cross-origin',
        'unsafe-url'
    ]):
        raise ValueError('Invalid option(s) for Referrer-Policy (must be "no-referrer", "no-referrer-when-downgrade", "origin", "origin-when-cross-origin", "same-origin", "strict-origin", "strict-origin-when-cross-origin", "unsafe-url")')
    if app is not None:
        app.add_middleware(SetMiddleware, headers=[(b"Referrer-Policy", ", ".join(option).encode('latin-1'))])
    return (b"Referrer-Policy", ", ".join(option).encode('latin-1'))