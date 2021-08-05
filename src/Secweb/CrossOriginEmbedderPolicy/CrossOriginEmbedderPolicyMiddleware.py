'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021, Motagamwala Taha Arif Ali '''

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class CrossOriginEmbedderPolicy(BaseHTTPMiddleware):
    ''' CrossOriginEmbedderPolicy class sets Cross-Origin-Embedder-Policy header it takes one Parameter

    Example:
        app.add_middleware(CrossOriginEmbedderPolicy, Option={})

    Parameter:

    Option={} This is a dictionary'''
    def __init__(self, app: ASGIApp, Option: dict = {'Cross-Origin-Embedder-Policy': 'unsafe-none'}) -> None:
        super().__init__(app)
        self.Option = Option
        self.Policies = ['require-corp', 'unsafe-none']

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if self.Option['Cross-Origin-Embedder-Policy'] in self.Policies:
            response.headers['Cross-Origin-Embedder-Policy'] = self.Option['Cross-Origin-Embedder-Policy']
        else:
            raise SyntaxError('Cross-Origin-Embedder-Policy has 2 options 1> "unsafe-none" 2> "require-corp"')
        return response
