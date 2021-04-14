'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021, Motagamwala Taha Arif Ali '''

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class XContentTypeOptions(BaseHTTPMiddleware):
    ''' XContentTypeOptions sets the X-Content-Type-Options header it takes no parameter

    Example :
        app.add_middleware(XContentTypeOptions)'''
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        pass

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
