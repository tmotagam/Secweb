'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2022, Motagamwala Taha Arif Ali '''

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class xXSSProtection(BaseHTTPMiddleware):
    ''' xXSSProtection class sets X-XSS-Protection header it takes one Parameter

    Example:
        app.add_middleware(xXSSProtection, Option={})

    Parameter:

    Option={} This is a dictionary'''
    def __init__(self, app: ASGIApp, Option: dict = {'X-XSS-Protection': '0'}) -> None:
        super().__init__(app)
        self.Option = Option

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if self.Option['X-XSS-Protection'] == '0' or self.Option['X-XSS-Protection'] == '1' or self.Option['X-XSS-Protection'] == '1; mode=block' or '1; report=' in self.Option['X-XSS-Protection']:
            response.headers['X-XSS-Protection'] = self.Option['X-XSS-Protection']
        else:
            raise SyntaxError('X-XSS-Protection has 4 options 1> "0" 2> "1" 3> "1; mode=block" 4> "1; report=<Your Reporting Uri>"')
        return response
