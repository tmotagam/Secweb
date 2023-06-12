'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2023, Motagamwala Taha Arif Ali '''

from starlette.types import Scope, Receive, Send, ASGIApp, Message
from starlette.datastructures import MutableHeaders

class XDNSPrefetchControl:
    ''' XDNSPrefetchControl class sets X-DNS-Prefetch-Control header it takes one Parameter

    Example:
        app.add_middleware(XDNSPrefetchControl, Option={})

    Parameter:

    Option={} This is a dictionary'''
    def __init__(self, app: ASGIApp, Option: dict[str, str] = {'X-DNS-Prefetch-Control': 'off'}):
        self.app = app
        self.Option = Option
        if self.Option['X-DNS-Prefetch-Control'] != 'on' and self.Option['X-DNS-Prefetch-Control'] != 'off':
            raise SyntaxError('X-DNS-Prefetch-Control has two values only 1> "on" 2> "off"')

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_x_DNS_Prefetch_Control(message: Message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('X-DNS-Prefetch-Control', self.Option['X-DNS-Prefetch-Control'])

            await send(message)

        await self.app(scope, receive, set_x_DNS_Prefetch_Control)