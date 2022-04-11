'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2022, Motagamwala Taha Arif Ali '''

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class ClearSiteData(BaseHTTPMiddleware):
    ''' ClearSiteData class sets Clear-Site-Data header it takes two Parameter

    Example:
        app.add_middleware(ClearSiteData, Option={}, Routes=[])

    Parameter:

    Option={} This is a dictionary

    Routes=[] This is an Array'''
    def __init__(self, app: ASGIApp, Option: dict = {'cache': True, 'cookies': True, 'storage': True}, Routes: list = []) -> None:
        super().__init__(app)
        self.Option = Option
        self.Routes = Routes
        self.policyString = ''

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        self.policyString = ''
        option = dict(self.Option)
        if self.Routes.__len__() == 0:
            raise SyntaxError('Cannot Set Clear-Site-Data header if the routes are empty')
        response = await call_next(request)
        for url in self.Routes:
            if url == request.url.components.path:
                if '*' in option and option['*'] is True:
                    self.policyString += '"*"'; option.pop('*')
                if 'cache' in option and option['cache'] is True:
                    self.policyString += '"cache"' if list(option.keys()).__len__() == 1 else '"cache", '
                    option.pop('cache')
                if 'cookies' in option and option['cookies'] is True:
                    self.policyString += '"cookies"' if list(option.keys()).__len__() == 1 else '"cookies", '
                    option.pop('cookies')
                if 'storage' in option and option['storage'] is True:
                    self.policyString += '"storage"'
                    option.pop('storage')
                if list(option.keys()).__len__() != 0 :
                    raise SyntaxError('Clear-Site-Data has 4 options 1> "cache" 2> "cookies" 3> "storage" 4> "*"')
                response.headers['Clear-Site-Data'] = self.policyString
                break
            elif '{' in url:
                url = url.rpartition('{')[0]
                if url in request.url.components.path:
                    if '*' in option and option['*'] is True:
                        self.policyString += '"*"'
                        option.pop('*')
                    if 'cache' in option and option['cache'] is True:
                        self.policyString += '"cache"' if list(option.keys()).__len__() == 1 else '"cache", '
                        option.pop('cache')
                    if 'cookies' in option and option['cookies'] is True:
                        self.policyString += '"cookies"' if list(option.keys()).__len__() == 1 else '"cookies", '
                        option.pop('cookies')
                    if 'storage' in option and option['storage'] is True:
                        self.policyString += '"storage"'
                        option.pop('storage')
                    if list(option.keys()).__len__() != 0 :
                        raise SyntaxError('Clear-Site-Data has 4 options 1> "cache" 2> "cookies" 3> "storage" 4> "*"')
                    response.headers['Clear-Site-Data'] = self.policyString
                    break
        return response