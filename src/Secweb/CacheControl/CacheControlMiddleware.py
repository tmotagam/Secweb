'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2022, Motagamwala Taha Arif Ali '''

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class CacheControl(BaseHTTPMiddleware):
    ''' CacheControl class sets Cache-Control header it takes one Parameter

    Example:
        app.add_middleware(CacheControl, Option={})

    Parameter:

    Option={} This is a dictionary'''

    def __init__(self, app: ASGIApp, Option: dict = {'max-age': 86400, 'private': True}) -> None:
        super().__init__(app)
        self.Option = Option
        self.policyString = ''

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        self.policyString = ''
        option = dict(self.Option)
        response = await call_next(request)
        if 'max-age' in option and option['max-age'] >= 0:
            self.policyString += f'max-age={str(option["max-age"])}' if list(
                option.keys()).__len__() == 1 else f'max-age={str(option["max-age"])}, '
            option.pop('max-age')
        if 's-maxage' in option and option['s-maxage'] >= 0:
            self.policyString += f's-maxage={str(option["s-maxage"])}' if list(
                option.keys()).__len__() == 1 else f's-maxage={str(option["s-maxage"])}, '
            option.pop('s-maxage')
        if 'no-cache' in option and option['no-cache'] is True:
            self.policyString += 'no-cache' if list(
                option.keys()).__len__() == 1 else 'no-cache, '
            option.pop('no-cache')
        if 'no-store' in option and option['no-store'] is True:
            self.policyString += 'no-store' if list(
                option.keys()).__len__() == 1 else 'no-store, '
            option.pop('no-store')
        if 'no-transform' in option and option['no-transform'] is True:
            self.policyString += 'no-transform' if list(
                option.keys()).__len__() == 1 else 'no-transform, '
            option.pop('no-transform')
        if 'must-revalidate' in option and option['must-revalidate'] is True:
            self.policyString += 'must-revalidate' if list(
                option.keys()).__len__() == 1 else 'must-revalidate, '
            option.pop('must-revalidate')
        if 'proxy-revalidate' in option and option['proxy-revalidate'] is True:
            self.policyString += 'proxy-revalidate' if list(
                option.keys()).__len__() == 1 else 'proxy-revalidate, '
            option.pop('proxy-revalidate')
        if 'must-understand' in option and option['must-understand'] is True:
            self.policyString += 'must-understand' if list(
                option.keys()).__len__() == 1 else 'must-understand, '
            option.pop('must-understand')
        if 'private' in option and option['private'] is True:
            self.policyString += 'private' if list(
                option.keys()).__len__() == 1 else 'private, '
            option.pop('private')
        if 'public' in option and option['public'] is True:
            self.policyString += 'public' if list(
                option.keys()).__len__() == 1 else 'public, '
            option.pop('public')
        if 'immutable' in option and option['immutable'] is True:
            self.policyString += 'immutable' if list(
                option.keys()).__len__() == 1 else 'immutable, '
            option.pop('immutable')
        if 'stale-while-revalidate' in option and option['stale-while-revalidate'] > 0:
            self.policyString += f'stale-while-revalidate={str(option["stale-while-revalidate"])}' if list(
                option.keys()).__len__() == 1 else f'stale-while-revalidate={str(option["stale-while-revalidate"])}, '
            option.pop('stale-while-revalidate')
        if list(option.keys()).__len__() != 0:
            raise SyntaxError('Cache-Control has 12 options 1> "max-age" 2> "s-maxage" 3> "no-cache" 4> "no-store" 5> "no-transform" 6> "must-revalidate" 7> "proxy-revalidate" 8> "must-understand" 9> "private" 10> "public" 11> "immutable" 12> "stale-while-revalidate" ')
        response.headers['Cache-Control'] = self.policyString
        return response
