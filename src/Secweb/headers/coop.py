from __future__ import annotations
from typing import TYPE_CHECKING

from ..middleware import SetMiddleware

if TYPE_CHECKING:
    from .._types import Cross_Origin_Opener_Policy_Options
    from starlette.applications import Starlette

def Cross_Origin_Opener_Policy(app: Starlette | None = None, option: Cross_Origin_Opener_Policy_Options = 'same-origin') -> tuple[bytes, bytes]:
    """
    Sets the `Cross-Origin-Opener-Policy` (COOP) HTTP response header.

    The COOP header allows you to ensure a top-level document does not share a browsing context group with cross-origin documents.
    This helps process-isolate your document and attackers can't access your global object if they were to open it in a popup.

    Args:
        app (Starlette | None, optional): An optional Starlette application instance. 
            If provided, the COOP header is injected into the application via middleware. Defaults to None.
        option (Cross_Origin_Opener_Policy_Options, optional): The policy directive to apply.
            Valid values are: "same-origin", "same-origin-allow-popups", "unsafe-none", or "noopener-allow-popups".
            Defaults to 'same-origin'.

    Returns:
        tuple[bytes, bytes]: A tuple representing the header key and its computed value, 
            e.g., `(b"Cross-Origin-Opener-Policy", b"same-origin")`.

    Raises:
        ValueError: If an unsupported policy directive is provided.

    Example:
        >>> Cross_Origin_Opener_Policy(app, option="same-origin")
        (b'Cross-Origin-Opener-Policy', b'same-origin')
    """
    if option not in ('same-origin', 'same-origin-allow-popups', 'unsafe-none', 'noopener-allow-popups'):
        raise ValueError('Invalid option for Cross-Origin-Opener-Policy (must be "same-origin", "same-origin-allow-popups", "unsafe-none", or "noopener-allow-popups")')
    if app is not None:
        app.add_middleware(SetMiddleware, headers=[(b'Cross-Origin-Opener-Policy', option.encode('latin-1'))])
    return (b'Cross-Origin-Opener-Policy', option.encode('latin-1'))
