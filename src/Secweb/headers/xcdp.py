from __future__ import annotations
from typing import TYPE_CHECKING

from ..middleware import SetMiddleware

if TYPE_CHECKING:
    from starlette.applications import Starlette
    from .._types import X_Permitted_Cross_Domain_Policies_Options

def X_Permitted_Cross_Domain_Policies(app: Starlette | None = None, option: X_Permitted_Cross_Domain_Policies_Options = 'none') -> tuple[bytes, bytes]:
    """
    Sets the `X-Permitted-Cross-Domain-Policies` HTTP response header.

    A cross-domain policy file is an XML document that grants a web client, such as Adobe Flash Player 
    or Adobe Acrobat (though largely obsolete now), permission to handle data across domains.
    This header restricts which cross-domain policy files are allowed.

    Args:
        app (Starlette | None, optional): An optional Starlette application instance. 
            If provided, the header is injected into the application via middleware. Defaults to None.
        option (X_Permitted_Cross_Domain_Policies_Options, optional): The policy directive to apply.
            Valid values are: 'none', 'master-only', 'by-content-type', 'by-ftp-filename', 'all', or 'none-this-response'.
            Defaults to 'none'.

    Returns:
        tuple[bytes, bytes]: A tuple representing the header key and its computed value, 
            e.g., `(b"X-Permitted-Cross-Domain-Policies", b"none")`.

    Raises:
        ValueError: If an unsupported policy directive is provided.

    Example:
        >>> X_Permitted_Cross_Domain_Policies(app, option="master-only")
        (b'X-Permitted-Cross-Domain-Policies', b'master-only')
    """
    if option not in ('none', 'master-only', 'by-content-type', 'by-ftp-filename', 'all', 'none-this-response'):
        raise ValueError('Invalid option for X-Permitted-Cross-Domain-Policies (must be "none", "master-only", "by-content-type", "by-ftp-filename", "all", or "none-this-response")')
    if app is not None:
        app.add_middleware(SetMiddleware, headers=[(b'X-Permitted-Cross-Domain-Policies', option.encode('latin-1'))])
    return (b'X-Permitted-Cross-Domain-Policies', option.encode('latin-1'))
