'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2022, Motagamwala Taha Arif Ali '''

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class ReferrerPolicy(BaseHTTPMiddleware):
    ''' ReferrerPolicy class sets Referrer-Policy header it takes one Parameter

    Example:
        app.add_middleware(ReferrerPolicy, Option={})

    Parameter:

    Option={} This is a dictionary'''

    def __init__(self, app: ASGIApp, Option: dict = {'Referrer-Policy': 'strict-origin-when-cross-origin'}) -> None:
        super().__init__(app)
        self.Option = Option
        self.Policies = ['no-referrer', 'no-referrer-when-downgrade', 'origin', 'origin-when-cross-origin',
                         'same-origin', 'strict-origin', 'strict-origin-when-cross-origin', 'unsafe-url']

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if self.Option['Referrer-Policy'] in self.Policies:
            response.headers['Referrer-Policy'] = self.Option['Referrer-Policy']
        elif len(self.Option['Referrer-Policy']) == 2:
            if self.Option['Referrer-Policy'][0] in self.Policies and self.Option['Referrer-Policy'][1] in self.Policies:
                response.headers['Referrer-Policy'] = ', '.join(
                    self.Option['Referrer-Policy'])
        else:
            raise SyntaxError('Referrer-Policy has 8 options 1> "no-referrer" 2> "no-referrer-when-downgrade" 3> "origin" 4> "origin-when-cross-origin" 5> "same-origin" 6> "strict-origin" 7> "strict-origin-when-cross-origin" 8> "unsafe-url"')
        return response
