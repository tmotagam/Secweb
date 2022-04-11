'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2022, Motagamwala Taha Arif Ali '''

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class ExpectCt(BaseHTTPMiddleware):
    ''' ExpectCt class takes only one parameter Option for setting the Expect-CT header

    Example :
        app.add_middleware(ExpectCt, Option={})

    Parameter :

    Option={} This is a dictionary'''
    def __init__(self, app: ASGIApp, Option: dict = {'max-age': 123, 'enforce': False, 'report-uri': ''}) -> None:
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

            if 'enforce' in self.Option and self.Option['enforce'] is True:
                self.PolicyString += ', enforce'

            if 'report-uri' in self.Option and self.Option['report-uri'] != '':
                self.PolicyString += ', report-uri=' + '"' + str(self.Option['report-uri']) + '"'

            response.headers['Expect-CT'] = self.PolicyString
        else:
            raise SyntaxError('Expect-CT has 3 options 1> "max-age=<Age>" <- This is the compulsory option 2> "enforce" 3> "report-uri=<Your URI>"')
        return response
