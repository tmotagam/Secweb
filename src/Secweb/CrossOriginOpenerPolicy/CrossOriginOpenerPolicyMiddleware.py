'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021, Motagamwala Taha Arif Ali '''

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class CrossOriginOpenerPolicy(BaseHTTPMiddleware):
    ''' CrossOriginOpenerPolicy class sets Cross-Origin-Opener-Policy header it takes one Parameter

    Example:
        app.add_middleware(CrossOriginOpenerPolicy, Option={})

    Parameter:

    Option={} This is a dictionary'''
    def __init__(self, app: ASGIApp, Option: dict = {'Cross-Origin-Opener-Policy': 'unsafe-none'}) -> None:
        super().__init__(app)
        self.Option = Option
        self.Policies = ['unsafe-none', 'same-origin-allow-popups', 'same-origin']

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if self.Option['Cross-Origin-Opener-Policy'] in self.Policies:
            response.headers['Cross-Origin-Opener-Policy'] = self.Option['Cross-Origin-Opener-Policy']
        else:
            raise SyntaxError('Cross-Origin-Opener-Policy has 3 options 1> "unsafe-none" 2> "same-origin-allow-popups" 3> "same-origin"')
        return response
