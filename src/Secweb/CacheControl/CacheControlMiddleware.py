'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2025, Motagamwala Taha Arif Ali '''

from starlette.datastructures import MutableHeaders

class CacheControl:
    ''' CacheControl class sets Cache-Control header.

    Example:
        app.add_middleware(CacheControl, Option={})

    Parameter:
        Option (dict): Optional dictionary containing cache control options.
            - 'max-age' (int): The maximum age of the cache in seconds.
            - 's-maxage' (int): The maximum age of the shared cache in seconds.
            - 'no-cache' (bool): Specifies whether the cache should be bypassed.
            - 'no-store' (bool): Specifies whether the cache should not store any response.
            - 'no-transform' (bool): Specifies whether the cache should not transform the response.
            - 'must-revalidate' (bool): Specifies whether the cache must revalidate the response.
            - 'proxy-revalidate' (bool): Specifies whether the cache must revalidate the response on the proxy server.
            - 'must-understand' (bool): Specifies whether the cache must understand the response.
            - 'private' (bool): Specifies whether the cache response is specific to a user.
            - 'public' (bool): Specifies whether the cache response is public.
            - 'immutable' (bool): Specifies whether the cache response is immutable.
            - 'stale-while-revalidate' (int): The maximum age of stale content in seconds while revalidating.
    
    '''
    def __init__(self, app, Option = {'max-age': 86400, 'private': True }):
        """
        Initializes a new instance of the class.

        Parameters:
            app (object): The application object.
            Option (dict): Optional dictionary containing cache control options.
                - 'max-age' (int): The maximum age of the cache in seconds.
                - 's-maxage' (int): The maximum age of the shared cache in seconds.
                - 'no-cache' (bool): Specifies whether the cache should be bypassed.
                - 'no-store' (bool): Specifies whether the cache should not store any response.
                - 'no-transform' (bool): Specifies whether the cache should not transform the response.
                - 'must-revalidate' (bool): Specifies whether the cache must revalidate the response.
                - 'proxy-revalidate' (bool): Specifies whether the cache must revalidate the response on the proxy server.
                - 'must-understand' (bool): Specifies whether the cache must understand the response.
                - 'private' (bool): Specifies whether the cache response is specific to a user.
                - 'public' (bool): Specifies whether the cache response is public.
                - 'immutable' (bool): Specifies whether the cache response is immutable.
                - 'stale-while-revalidate' (int): The maximum age of stale content in seconds while revalidating.

        Raises:
            SyntaxError: If the `Option` dictionary contains unsupported cache control options.

        Returns:
            None
        """
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
        """
        Asynchronously handles HTTP requests by routing them to the appropriate handler based on the request path.

        Parameters:
            scope (Dict[str, Any]): The scope of the request.
            receive (Callable[[], Awaitable[Dict[str, Any]]]): A function that returns a coroutine that reads messages from the server.
            send (Callable[[Dict[str, Any]], Awaitable[None]]): A function that sends messages to the server.

        Returns:
            None
        """
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_Cache_Control(message):
            """
            Set the Cache-Control header in the HTTP response.

            Parameters:
                message (dict): The message object containing the response information.

            Returns:
                None
            """
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('Cache-Control', self.policyString)

            await send(message)

        await self.app(scope, receive, set_Cache_Control)