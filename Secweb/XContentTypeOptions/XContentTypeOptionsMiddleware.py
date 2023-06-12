'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2023, Motagamwala Taha Arif Ali '''

from starlette.types import Scope, Receive, Send, ASGIApp, Message
from starlette.datastructures import MutableHeaders

class XContentTypeOptions:
    ''' XContentTypeOptions sets the X-Content-Type-Options header it takes no parameter

    Example :
        app.add_middleware(XContentTypeOptions)'''
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_x_Content_Type_Options(message: Message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('X-Content-Type-Options', 'nosniff')

            await send(message)

        await self.app(scope, receive, set_x_Content_Type_Options)