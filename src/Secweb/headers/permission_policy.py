from __future__ import annotations
from typing import TYPE_CHECKING
from warnings import warn

from ..middleware import SetMiddleware

if TYPE_CHECKING:
    from .._types import Permissions_Policy_Options
    from starlette.applications import Starlette

VALID_PERMISSIONS_POLICY = [
    "accelerometer", "ambient-light-sensor", "aria-notify", "attribution-reporting", 
    "autoplay", "bluetooth", "browsing-topics", "camera", "captured-surface-control", "ch-ua-high-entropy-values", 
    "compute-pressure", "cross-origin-isolated", "deferred-fetch", "deferred-fetch-minimal", 
    "display-capture", "encrypted-media", "fullscreen", "geolocation", "gyroscope", "hid", 
    "identity-credentials-get", "idle-detection", "local-fonts", "local-network", "local-network-access", "loopback-network", 
    "magnetometer", "microphone", "midi", "on-device-speech-recognition", "otp-credentials", "payment", "picture-in-picture", 
    "private-state-token-issuance", "private-state-token-redemption", "publickey-credentials-create", 
    "publickey-credentials-get", "screen-wake-lock", "serial", "storage-access", "summarizer", 
    "usb", "web-share", "window-management", "xr-spatial-tracking"
]

def Permissions_Policy(
    app: Starlette | None = None, 
    options: Permissions_Policy_Options | None = None
) -> tuple[bytes, bytes]:
    """
    Sets the `Permissions-Policy` HTTP response header.

    The `Permissions-Policy` header provides a mechanism to allow and deny the use of browser features 
    in its own frame, and in content within any `<iframe>` elements in the document. 
    (Note: This header is still under a working draft and browsers may yield warnings).

    Args:
        app (Starlette | None, optional): An optional Starlette application instance. 
            If provided, the header is injected into the application via middleware. Defaults to None.
        options (Permissions_Policy_Options | None, optional): A dictionary mapping permission features 
            to lists of allowed origins/values. Must not be empty. Defaults to None.

    Returns:
        tuple[bytes, bytes]: A tuple representing the header key and its computed value, 
            e.g., `(b"Permissions-Policy", b"geolocation=(self), camera=()")`.

    Raises:
        ValueError: If `options` is empty or None.
        ValueError: If an invalid/unsupported policy feature is provided.
        ValueError: If the feature value is not a list.
        ValueError: If a wildcard ('*') is mixed with other origin items.
        ValueError: If an allowlist item is improperly formatted (must be '*', 'self', or a quoted URL).

    Example:
        >>> Permissions_Policy(app, options={"geolocation": ["self", '"https://example.com"'], "camera": []})
        (b'Permissions-Policy', b'geolocation=(self "https://example.com"), camera=()')
    """
    
    if not options:
        raise ValueError('options cannot be empty for Permissions-Policy to be applied')
        
    warn("Permissions-Policy header is still under working draft, browsers might give warnings and errors", SyntaxWarning, stacklevel=2)
    
    parts: list[str] = []
    
    for key, values in options.items():
        if key not in VALID_PERMISSIONS_POLICY:
            raise ValueError(f'The Policy {key} does not exist')
            
        if not isinstance(values, list):
            raise ValueError(f"Value for {key} must be a list")

        if len(values) != 1 and "*" in values:
            raise ValueError('Cannot use wildcard(*) with other allowlist items.')

        if "*" in values:
            parts.append(f"{key}=*")
            continue
            
        if len(values) == 0:
            parts.append(f"{key}=()")
            continue
            
        allowlist: list[str] = []
        for val in values:
            value = str(val)
            if value != "self" and not value.startswith('"'):
                raise ValueError(f'Invalid allowlist item({value}) for feature {key}. Allowlist item must be *, self or a quoted URL "https://example.com"')
            allowlist.append(value)
            
        parts.append(f"{key}=({' '.join(allowlist)})")
        
    policy_bytes = ", ".join(parts).encode('latin-1')
    header_name = b'Permissions-Policy'
    
    if app is not None:
        app.add_middleware(SetMiddleware, headers=[(header_name, policy_bytes)])
        
    return (header_name, policy_bytes)
