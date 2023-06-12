'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2023, Motagamwala Taha Arif Ali '''

from starlette.types import Scope, Receive, Send, ASGIApp, Message
from starlette.datastructures import MutableHeaders

class CrossOriginOpenerPolicy:
    ''' CrossOriginOpenerPolicy class sets Cross-Origin-Opener-Policy header it takes one Parameter

    Example:
        app.add_middleware(CrossOriginOpenerPolicy, Option={})

    Parameter:

    Option={} This is a dictionary'''
    def __init__(self, app: ASGIApp, Option: dict[str, str] = {'Cross-Origin-Opener-Policy': 'unsafe-none'}):
        self.app = app
        self.Option = Option
        Policies = ['unsafe-none', 'same-origin-allow-popups', 'same-origin']
        if self.Option['Cross-Origin-Opener-Policy'] not in Policies:
            raise SyntaxError('Cross-Origin-Opener-Policy has 3 options 1> "unsafe-none" 2> "same-origin-allow-popups" 3> "same-origin"')

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_Cross_Origin_Opener_Policy(message: Message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('Cross-Origin-Opener-Policy', self.Option['Cross-Origin-Opener-Policy'])

            await send(message)

        await self.app(scope, receive, set_Cross_Origin_Opener_Policy)