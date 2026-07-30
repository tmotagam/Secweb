from __future__ import annotations
from typing import TYPE_CHECKING
from functools import wraps

from ..middleware import SetMiddleware

if TYPE_CHECKING:
    from .._types import Clear_Site_Data_Options
    from starlette.types import ASGIApp
    from starlette.requests import Request
    from starlette.responses import Response

def Clear_Site_Data(options: Clear_Site_Data_Options = {'*': True}):
    """
    A decorator to set the `Clear-Site-Data` HTTP response header for specific route handlers.

    The `Clear-Site-Data` header clears browsing data (cookies, storage, cache) associated with the requesting website. 
    It allows web developers to have more control over the data stored by a client browser for their origins.

    Args:
        options (Clear_Site_Data_Options, optional): A dictionary specifying which data types to clear. 
            Keys can be '*', 'cache', 'cookies', 'storage', 'prefetchCache', 'prerenderCache', 'clientHints'.
            If '*' is set to True, all types are cleared. Defaults to {'*': True}.

    Returns:
        Callable: A decorator function that wraps the route handler and injects the header into its response.

    Raises:
        ValueError: If no valid clear options are enabled.

    Example:
        @app.get('/logout')
        @Clear_Site_Data(options={'cookies': True, 'storage': True})
        async def logout():
            return {"message": "Logged out successfully"}
    """
    parts: list[str] = []
    
    if '*' in options and options['*'] is True:
        parts.append('"*"')
    else:
        if options.get('cache'):
            parts.append('"cache"')
        if options.get('cookies'):
            parts.append('"cookies"')
        if options.get('storage'):
            parts.append('"storage"')
        if options.get('prefetchCache'):
            parts.append('"prefetchCache"')
        if options.get('prerenderCache'):
            parts.append('"prerenderCache"')
        if options.get('clientHints'):
            parts.append('"clientHints"')
            
    if not parts:
        raise ValueError('Clear-Site-Data must have at least one option enabled.')
        
    policy_string = ", ".join(parts)
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            from starlette.responses import Response as StarletteResponse
            result = func(*args, **kwargs)
            
            if hasattr(result, '__await__'):
                result = await result
            
            if isinstance(result, StarletteResponse):
                result.headers['Clear-Site-Data'] = policy_string
                return result
            else:
                from fastapi.responses import JSONResponse
                response = JSONResponse(content=result)
                response.headers['Clear-Site-Data'] = policy_string
                return response
        return wrapper
    return decorator
