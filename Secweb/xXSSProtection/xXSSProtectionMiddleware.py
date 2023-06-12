'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2023, Motagamwala Taha Arif Ali '''

from starlette.types import Scope, Receive, Send, ASGIApp, Message
from starlette.datastructures import MutableHeaders

class xXSSProtection:
    ''' xXSSProtection class sets X-XSS-Protection header it takes one Parameter

    Example:
        app.add_middleware(xXSSProtection, Option={})

    Parameter:

    Option={} This is a dictionary'''
    def __init__(self, app: ASGIApp, Option: dict[str, str] = {'X-XSS-Protection': '0'}):
        self.app = app
        self.Option = Option
        if self.Option['X-XSS-Protection'] != '0' and self.Option['X-XSS-Protection'] != '1' and self.Option['X-XSS-Protection'] != '1; mode=block' and '1; report=' not in self.Option['X-XSS-Protection']:
            raise SyntaxError('X-XSS-Protection has 4 options 1> "0" 2> "1" 3> "1; mode=block" 4> "1; report=<Your Reporting Uri>"')

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_x_XSS_Protection(message: Message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('X-XSS-Protection', self.Option['X-XSS-Protection'])

            await send(message)

        await self.app(scope, receive, set_x_XSS_Protection)