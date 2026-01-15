'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2026, Motagamwala Taha Arif Ali '''

from typing import Literal, Union
from warnings import warn
from starlette.datastructures import MutableHeaders
from starlette.types import Send, Receive, Scope, Message, ASGIApp

XDNSPrefetchControlLiteral = Literal['on', 'off']

XDNSPrefetchControlOptions = Union[dict[Literal['X-DNS-Prefetch-Control'], XDNSPrefetchControlLiteral], XDNSPrefetchControlLiteral]

class XDNSPrefetchControl:
    ''' XDNSPrefetchControl class sets X-DNS-Prefetch-Control header.

    Example:
        app.add_middleware(XDNSPrefetchControl, Option='')

    Parameter:
        Option (XDNSPrefetchControlOptions, Optional):
            - 'on': Sets the value of the `X-DNS-Prefetch-Control` header to 'on'.
            - 'off': Sets the value of the `X-DNS-Prefetch-Control` header to 'off'. (Default)
    
    '''
    def __init__(self, app: ASGIApp, Option: XDNSPrefetchControlOptions = 'off'):
        """
        Initializes the class object.

        Parameters:
            app (ASGIApp): The application object.
            Option (XDNSPrefetchControlOptions, Optional):
                - 'on': Sets the value of the `X-DNS-Prefetch-Control` header to 'on'.
                - 'off': Sets the value of the `X-DNS-Prefetch-Control` header to 'off'. (Default)

        Raises:
            SyntaxError: If the value of the Option is neither 'on' nor 'off'.
        """
        self.app = app
        self.Option = Option
        if not isinstance(self.Option, str):
            warn('XDNSPrefetchControl middleware will now accept string rather than dictonary eg. Option={"X-DNS-Prefetch-Control": "off"} will be Option="off"', SyntaxWarning, 2)
            if self.Option['X-DNS-Prefetch-Control'] != 'on' and self.Option['X-DNS-Prefetch-Control'] != 'off':
                raise SyntaxError('X-DNS-Prefetch-Control has two values only 1> "on" 2> "off"')
        else:
            if self.Option != 'on' and self.Option != 'off':
                raise SyntaxError('XDNSPrefetchControl has two values only 1> "on" 2> "off"') 

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

        async def set_x_DNS_Prefetch_Control(message: Message):
            """
            Sets the value of the `X-DNS-Prefetch-Control` header in the response headers.

            Parameters:
                message (dict): The message object received from the server.

            Returns:
                None
            """
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('X-DNS-Prefetch-Control', self.Option if isinstance(self.Option, str) else self.Option['X-DNS-Prefetch-Control'])

            await send(message)

        await self.app(scope, receive, set_x_DNS_Prefetch_Control)