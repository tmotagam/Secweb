from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from starlette.types import ASGIApp, Message, Receive, Scope, Send


class _SetHeadersMiddleware:
    """
    An internal ASGI middleware class that appends HTTP response headers and WebSocket headers to requests.
    """
    def __init__(self, app: ASGIApp, headers: list[tuple[bytes, bytes]], wshsts: tuple[bytes, bytes] | None = None, dynamic_headers: list | None = None):
        """
        Initializes the middleware.

        Args:
            app (ASGIApp): The ASGI application to wrap.
            headers (list[tuple[bytes, bytes]]): A list of static HTTP headers (key-value pairs) to append.
            wshsts (tuple[bytes, bytes] | None, optional): An optional HSTS header for WebSocket connections. Defaults to None.
            dynamic_headers (list | None, optional): A list of callables that return dynamic headers (like nonces) per request. Defaults to None.
        """
        self.app = app
        self.headers = headers
        self.wshsts = wshsts
        self.dynamic_headers = dynamic_headers or []

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """
        Processes the incoming ASGI scope and attaches the configured headers to the HTTP or WebSocket response.
        """
        if scope["type"] not in ("http", "websocket"):
            return await self.app(scope, receive, send)

        if scope["type"] == "websocket" and self.wshsts is None:
            return await self.app(scope, receive, send)

        async def setheaders(message: Message):
            if message["type"] == "http.response.start":
                message.setdefault("headers", []).extend(self.headers)
                
                if self.dynamic_headers:
                    for get_header in self.dynamic_headers:
                        message["headers"].append(get_header())
            
            if message["type"] == "websocket.accept":
                message.setdefault("headers", []).append(self.wshsts)

            await send(message)

        await self.app(scope, receive, setheaders)

def SetMiddleware(app: ASGIApp, headers: list[tuple[bytes, bytes]], wshsts: tuple[bytes, bytes] | None = None, dynamic_headers: list | None = None):
    """
    A factory function to create or extend the `_SetHeadersMiddleware`.
    
    If the application is already wrapped by `_SetHeadersMiddleware`, this function 
    extends its existing configuration rather than creating a nested middleware layer.

    Args:
        app (ASGIApp): The ASGI application.
        headers (list[tuple[bytes, bytes]]): Additional static headers to apply.
        wshsts (tuple[bytes, bytes] | None, optional): An additional WebSocket HSTS header. Defaults to None.
        dynamic_headers (list | None, optional): Additional dynamic header callables. Defaults to None.

    Returns:
        _SetHeadersMiddleware: The initialized or updated middleware instance.
        
    Example:
        >>> app = SetMiddleware(app, headers=[(b'X-My-Header', b'value')])
    """
    if isinstance(app, _SetHeadersMiddleware):
        app.headers.extend(headers)
        if wshsts is not None:
            app.wshsts = wshsts
        if dynamic_headers is not None:
            app.dynamic_headers.extend(dynamic_headers)
        return app
    return _SetHeadersMiddleware(app, headers, wshsts, dynamic_headers)
