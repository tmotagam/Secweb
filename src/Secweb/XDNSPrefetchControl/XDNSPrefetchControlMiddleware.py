'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021, Motagamwala Taha Arif Ali '''

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class XDNSPrefetchControl(BaseHTTPMiddleware):
    ''' XDNSPrefetchControl class sets X-DNS-Prefetch-Control header it takes one Parameter

    Example:
        app.add_middleware(XDNSPrefetchControl, Option={})

    Parameter:

    Option={} This is a dictionary'''
    def __init__(self, app: ASGIApp, Option: dict = {'X-DNS-Prefetch-Control': 'off'}) -> None:
        super().__init__(app)
        self.Option = Option

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if self.Option['X-DNS-Prefetch-Control'] == 'on' or self.Option['X-DNS-Prefetch-Control'] == 'off':
            response.headers['X-DNS-Prefetch-Control'] = self.Option['X-DNS-Prefetch-Control']
        else:
            raise SyntaxError('X-DNS-Prefetch-Control has two values only 1> "on" 2> "off"')
        return response
