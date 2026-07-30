from __future__ import annotations
from typing import TYPE_CHECKING

from ..middleware import SetMiddleware

if TYPE_CHECKING:
    from starlette.applications import Starlette

def Origin_Agent_Cluster(app: Starlette | None = None) -> tuple[bytes, bytes]:
    """
    Sets the `Origin-Agent-Cluster` HTTP response header.

    The `Origin-Agent-Cluster` header instructs the browser to parse the document in an origin-keyed 
    agent cluster. This provides better isolation by separating cross-origin but same-site pages 
    into different processes, which can mitigate certain cross-origin side-channel attacks like Spectre.

    Args:
        app (Starlette | None, optional): An optional Starlette application instance. 
            If provided, the `Origin-Agent-Cluster: ?1` header is injected into the application via middleware. Defaults to None.

    Returns:
        tuple[bytes, bytes]: A tuple representing the header key and its computed value, 
            which is always `(b"Origin-Agent-Cluster", b"?1")`.

    Example:
        >>> Origin_Agent_Cluster(app)
        (b'Origin-Agent-Cluster', b'?1')
    """
    if app is not None:
        app.add_middleware(SetMiddleware, headers=[(b'Origin-Agent-Cluster', b'?1')])
    return (b'Origin-Agent-Cluster', b'?1')
