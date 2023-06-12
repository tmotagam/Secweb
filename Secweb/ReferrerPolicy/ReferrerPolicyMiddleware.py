'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2023, Motagamwala Taha Arif Ali '''

from starlette.types import Scope, Receive, Send, ASGIApp, Message
from starlette.datastructures import MutableHeaders

class ReferrerPolicy:
    ''' ReferrerPolicy class sets Referrer-Policy header it takes one Parameter

    Example:
        app.add_middleware(ReferrerPolicy, Option={})

    Parameter:

    Option={} This is a dictionary'''
    def __init__(self, app: ASGIApp, Option: dict[str, str | list[str]] = {'Referrer-Policy': 'strict-origin-when-cross-origin'}):
        self.app = app
        Policies = ['no-referrer', 'no-referrer-when-downgrade', 'origin', 'origin-when-cross-origin', 'same-origin', 'strict-origin', 'strict-origin-when-cross-origin', 'unsafe-url']
        self.policystring = ''
        if Option['Referrer-Policy'] in Policies:
            self.policystring = Option['Referrer-Policy']
        elif len(Option['Referrer-Policy']) > 1:
            for option in Option['Referrer-Policy']:
                if option not in Policies:
                    raise SyntaxError('Referrer-Policy has 8 options 1> "no-referrer" 2> "no-referrer-when-downgrade" 3> "origin" 4> "origin-when-cross-origin" 5> "same-origin" 6> "strict-origin" 7> "strict-origin-when-cross-origin" 8> "unsafe-url"')
            self.policystring = ', '.join(Option['Referrer-Policy'])
        else:
            raise SyntaxError('Referrer-Policy has 8 options 1> "no-referrer" 2> "no-referrer-when-downgrade" 3> "origin" 4> "origin-when-cross-origin" 5> "same-origin" 6> "strict-origin" 7> "strict-origin-when-cross-origin" 8> "unsafe-url"')

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_Referrer_Policy(message: Message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('Referrer-Policy', self.policystring)

            await send(message)

        await self.app(scope, receive, set_Referrer_Policy)