'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2023, Motagamwala Taha Arif Ali '''

from starlette.datastructures import MutableHeaders

class CacheControl:
    ''' CacheControl class sets Cache-Control header it takes one Parameter

    Example:
        app.add_middleware(CacheControl, Option={})

    Parameter:

    Option={} This is a dictionary'''
    def __init__(self, app, Option = {'max-age': 86400, 'private': True }):
        self.app = app
        self.policyString = ''
        if 'max-age' in Option and Option['max-age'] >= 0:
            self.policyString += f'max-age={str(Option["max-age"])}' if list(Option.keys()).__len__() == 1 else f'max-age={str(Option["max-age"])}, '
            Option.pop('max-age')
        if 's-maxage' in Option and Option['s-maxage'] >= 0:
            self.policyString += f's-maxage={str(Option["s-maxage"])}' if list(Option.keys()).__len__() == 1 else f's-maxage={str(Option["s-maxage"])}, '
            Option.pop('s-maxage')
        if 'no-cache' in Option and Option['no-cache'] is True:
            self.policyString += 'no-cache' if list(Option.keys()).__len__() == 1 else 'no-cache, '
            Option.pop('no-cache')
        if 'no-store' in Option and Option['no-store'] is True:
            self.policyString += 'no-store' if list(Option.keys()).__len__() == 1 else 'no-store, '
            Option.pop('no-store')
        if 'no-transform' in Option and Option['no-transform'] is True:
            self.policyString += 'no-transform' if list(Option.keys()).__len__() == 1 else 'no-transform, '
            Option.pop('no-transform')
        if 'must-revalidate' in Option and Option['must-revalidate'] is True:
            self.policyString += 'must-revalidate' if list(Option.keys()).__len__() == 1 else 'must-revalidate, '
            Option.pop('must-revalidate')
        if 'proxy-revalidate' in Option and Option['proxy-revalidate'] is True:
            self.policyString += 'proxy-revalidate' if list(Option.keys()).__len__() == 1 else 'proxy-revalidate, '
            Option.pop('proxy-revalidate')
        if 'must-understand' in Option and Option['must-understand'] is True:
            self.policyString += 'must-understand' if list(Option.keys()).__len__() == 1 else 'must-understand, '
            Option.pop('must-understand')
        if 'private' in Option and Option['private'] is True:
            self.policyString += 'private' if list(Option.keys()).__len__() == 1 else 'private, '
            Option.pop('private')
        if 'public' in Option and Option['public'] is True:
            self.policyString += 'public' if list(Option.keys()).__len__() == 1 else 'public, '
            Option.pop('public')
        if 'immutable' in Option and Option['immutable'] is True:
            self.policyString += 'immutable' if list(Option.keys()).__len__() == 1 else 'immutable, '
            Option.pop('immutable')
        if 'stale-while-revalidate' in Option and Option['stale-while-revalidate'] > 0:
            self.policyString += f'stale-while-revalidate={str(Option["stale-while-revalidate"])}' if list(Option.keys()).__len__() == 1 else f'stale-while-revalidate={str(Option["stale-while-revalidate"])}, '
            Option.pop('stale-while-revalidate')
        if list(Option.keys()).__len__() != 0 :
            raise SyntaxError('Cache-Control has 12 options 1> "max-age" 2> "s-maxage" 3> "no-cache" 4> "no-store" 5> "no-transform" 6> "must-revalidate" 7> "proxy-revalidate" 8> "must-understand" 9> "private" 10> "public" 11> "immutable" 12> "stale-while-revalidate" ')

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_Cache_Control(message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('Cache-Control', self.policyString)

            await send(message)

        await self.app(scope, receive, set_Cache_Control)