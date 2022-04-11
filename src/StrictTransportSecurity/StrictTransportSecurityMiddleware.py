'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2022, Motagamwala Taha Arif Ali '''

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class HSTS(BaseHTTPMiddleware):
    ''' HSTS class sets Strict-Transport-Security Header it takes one parameter

    Example :
        app.add_middleware(HSTS, Option={})

    Parameter :

    Option={} This is a dictionary'''
    def __init__(self, app: ASGIApp, Option: dict = {'max-age': 432000, 'includeSubDomains': True, 'preload': False}) -> None:
        super().__init__(app)
        self.Option = Option
        self.PolicyString = ''

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        self.PolicyString = ''
        response = await call_next(request)
        if 'max-age' in self.Option:
            if int(self.Option['max-age']) and self.Option['max-age'] > 0:
                self.PolicyString += 'max-age=' + str(self.Option['max-age'])
            else:
                raise SyntaxError('max-age needs to be a positive integer')

            try:
                if self.Option['includeSubDomains'] is not False:
                    self.PolicyString += '; includeSubDomains'
            except KeyError:
                self.PolicyString += '; includeSubDomains'

            if 'preload' in self.Option and self.Option['preload'] is True:
                self.PolicyString += '; preload'

            response.headers['Strict-Transport-Security'] = self.PolicyString

        else:
            raise SyntaxError('Strict-Transport-Security has 3 options 1> "max-age=<expire-time>" <- This is the compulsory option 2> "includeSubDomains" 3> "preload"')
        return response
