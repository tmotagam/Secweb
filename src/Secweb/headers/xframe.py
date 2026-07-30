from __future__ import annotations
from typing import TYPE_CHECKING

from ..middleware import SetMiddleware

if TYPE_CHECKING:
    from starlette.applications import Starlette
    from .._types import X_Frame_Options

def X_Frame(app: Starlette | None = None, option: X_Frame_Options = 'SAMEORIGIN') -> tuple[bytes, bytes]:
    """
    Sets the `X-Frame-Options` HTTP response header.

    The `X-Frame-Options` header can be used to indicate whether or not a browser should be allowed 
    to render a page in a `<frame>`, `<iframe>`, `<embed>` or `<object>`. Sites can use this to avoid 
    clickjacking attacks, by ensuring that their content is not embedded into other sites.

    Args:
        app (Starlette | None, optional): An optional Starlette application instance. 
            If provided, the header is injected into the application via middleware. Defaults to None.
        option (X_Frame_Options, optional): The policy directive to apply.
            Valid values are: "SAMEORIGIN" or "DENY". Defaults to 'SAMEORIGIN'.

    Returns:
        tuple[bytes, bytes]: A tuple representing the header key and its computed value, 
            e.g., `(b"X-Frame-Options", b"SAMEORIGIN")`.

    Raises:
        ValueError: If an unsupported policy directive is provided.

    Example:
        >>> X_Frame(app, option="DENY")
        (b'X-Frame-Options', b'DENY')
    """
    if option not in ('SAMEORIGIN', 'DENY'):
        raise ValueError('Invalid option for X-Frame-Options (must be "SAMEORIGIN" or "DENY")')
    if app is not None:
        app.add_middleware(SetMiddleware, headers=[(b'X-Frame-Options', option.encode('latin-1'))])
    return (b'X-Frame-Options', option.encode('latin-1'))
