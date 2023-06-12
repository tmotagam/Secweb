'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2023, Motagamwala Taha Arif Ali '''

from starlette.types import Scope, Receive, Send, ASGIApp, Message
from starlette.datastructures import MutableHeaders

class XFrame:
    ''' XFrame class sets X-Frame-Options header it takes one Parameter

    Example:
        app.add_middleware(XFrame, Option={})

    Parameter:

    Option={} This is a dictionary'''
    def __init__(self, app: ASGIApp, Option: dict[str, str] = {'X-Frame-Options': 'DENY'}):
        self.app = app
        self.Option = Option
        if self.Option['X-Frame-Options'] != 'SAMEORIGIN' and self.Option['X-Frame-Options'] != 'DENY':
            raise SyntaxError('X-Frame-Options has two values only 1> "DENY" 2> "SAMEORIGIN"')

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_x_Frame_Options(message: Message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('X-Frame-Options', self.Option['X-Frame-Options'])

            await send(message)

        await self.app(scope, receive, set_x_Frame_Options)