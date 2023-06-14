'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2023, Motagamwala Taha Arif Ali '''

from starlette.datastructures import MutableHeaders

class CrossOriginResourcePolicy:
    ''' CrossOriginResourcePolicy class sets Cross-Origin-Resource-Policy header it takes one Parameter

    Example:
        app.add_middleware(CrossOriginResourcePolicy, Option={})

    Parameter:

    Option={} This is a dictionary'''
    def __init__(self, app, Option = {'Cross-Origin-Resource-Policy': 'cross-origin'}):
        self.app = app
        self.Option = Option
        Policies = ['same-site', 'same-origin', 'cross-origin']
        if self.Option['Cross-Origin-Resource-Policy'] not in Policies:
            raise SyntaxError('Cross-Origin-Resource-Policy has 3 options 1> "same-site" 2> "same-origin" 3> "cross-origin"')

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_Cross_Origin_Resource_Policy(message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('Cross-Origin-Resource-Policy', self.Option['Cross-Origin-Resource-Policy'])

            await send(message)

        await self.app(scope, receive, set_Cross_Origin_Resource_Policy)