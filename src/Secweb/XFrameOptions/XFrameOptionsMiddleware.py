'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2022, Motagamwala Taha Arif Ali '''

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class XFrame(BaseHTTPMiddleware):
    ''' XFrame class sets X-Frame-Options header it takes one Parameter

    Example:
        app.add_middleware(XFrame, Option={})

    Parameter:

    Option={} This is a dictionary'''

    def __init__(self, app: ASGIApp, Option: dict = {'X-Frame-Options': 'DENY'}) -> None:
        super().__init__(app)
        self.Option = Option

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if self.Option['X-Frame-Options'] == 'SAMEORIGIN' or self.Option['X-Frame-Options'] == 'DENY':
            response.headers['X-Frame-Options'] = self.Option['X-Frame-Options']
        else:
            raise SyntaxError(
                'X-Frame-Options has two values only 1> "DENY" 2> "SAMEORIGIN"')
        return response
