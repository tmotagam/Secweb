'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2026, Motagamwala Taha Arif Ali '''

from starlette.datastructures import MutableHeaders
from starlette.types import Send, Receive, Scope, Message, ASGIApp


class XDownloadOptions:
    ''' XDownloadOptions sets the X-Download-Options header.

    Example :
        app.add_middleware(XDownloadOptions)
    
    '''
    def __init__(self, app: ASGIApp):
        """
        Initializes a new instance of the class.

        :param app: The app object.
        """
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """
        Asynchronously handles HTTP requests by routing them to the appropriate handler based on the request path.

        Parameters:
            scope (Scope): The scope of the request.
            receive (Receive): A function that returns a coroutine that reads messages from the server.
            send (Send): A function that sends messages to the server.

        Returns:
            None
        """
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_x_Download_Options(message: Message):
            """
            Set the X-Download-Options header in the HTTP response header.

            Args:
                message (dict): The message received from the server.

            Returns:
                None
            """
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('X-Download-Options', 'noopen')

            await send(message)

        await self.app(scope, receive, set_x_Download_Options)