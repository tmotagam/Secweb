'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2022, Motagamwala Taha Arif Ali '''

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class CrossOriginResourcePolicy(BaseHTTPMiddleware):
    ''' CrossOriginResourcePolicy class sets Cross-Origin-Resource-Policy header it takes one Parameter

    Example:
        app.add_middleware(CrossOriginResourcePolicy, Option={})

    Parameter:

    Option={} This is a dictionary'''

    def __init__(self, app: ASGIApp, Option: dict = {'Cross-Origin-Resource-Policy': 'cross-origin'}) -> None:
        super().__init__(app)
        self.Option = Option
        self.Policies = ['same-site', 'same-origin', 'cross-origin']

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if self.Option['Cross-Origin-Resource-Policy'] in self.Policies:
            response.headers['Cross-Origin-Resource-Policy'] = self.Option['Cross-Origin-Resource-Policy']
        else:
            raise SyntaxError(
                'Cross-Origin-Resource-Policy has 3 options 1> "same-site" 2> "same-origin" 3> "cross-origin"')
        return response
