'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2026, Motagamwala Taha Arif Ali '''

from typing import Literal, Union
from warnings import warn
from starlette.types import Send, Receive, Scope, Message, ASGIApp

from starlette.datastructures import MutableHeaders

CrossOriginOpenerPolicyLiteral = Literal['unsafe-none', 'same-origin-allow-popups', 'same-origin', 'noopener-allow-popups']

CrossOriginOpenerPolicyOptions = Union[dict[Literal['Cross-Origin-Opener-Policy'], CrossOriginOpenerPolicyLiteral], CrossOriginOpenerPolicyLiteral]

class CrossOriginOpenerPolicy:
    ''' CrossOriginOpenerPolicy class sets Cross-Origin-Opener-Policy header.

    Example:
        app.add_middleware(CrossOriginOpenerPolicy, Option='')

    Parameter:
        Option (CrossOriginOpenerPolicyOptions, optional):
            - 'unsafe-none': Sets the Cross-Origin-Opener-Policy header to 'unsafe-none' (Default).
            - 'same-origin-allow-popups': Sets the Cross-Origin-Opener-Policy header to 'same-origin-allow-popups'.
            - 'same-origin': Sets the Cross-Origin-Opener-Policy header to 'same-origin'.
            - 'noopener-allow-popups': Sets the Cross-Origin-Opener-Policy header to 'noopener-allow-popups'.
    
    '''
    def __init__(self, app: ASGIApp, Option: CrossOriginOpenerPolicyOptions = 'unsafe-none'):
        """
        Initializes an instance of the class.

        Args:
            app (ASGIApp): The app object.
            Option (CrossOriginOpenerPolicyOptions, optional):
                - 'unsafe-none': Sets the Cross-Origin-Opener-Policy header to 'unsafe-none' (Default).
                - 'same-origin-allow-popups': Sets the Cross-Origin-Opener-Policy header to 'same-origin-allow-popups'.
                - 'same-origin': Sets the Cross-Origin-Opener-Policy header to 'same-origin'.
                - 'noopener-allow-popups': Sets the Cross-Origin-Opener-Policy header to 'noopener-allow-popups'.

        Raises:
            SyntaxError: If the value of Option is not one of the allowed policies.

        Returns:
            None
        """
        self.app = app
        self.Option = Option
        Policies = ['unsafe-none', 'same-origin-allow-popups', 'same-origin', 'noopener-allow-popups']
        if not isinstance(self.Option, str):
            warn('CrossOriginOpenerPolicy middleware will now accept string rather than dictonary eg. Option={"Cross-Origin-Opener-Policy": "unsafe-none"} will be Option="unsafe-none"', SyntaxWarning, 2)
            if self.Option['Cross-Origin-Opener-Policy'] not in Policies:
                raise SyntaxError('Cross-Origin-Opener-Policy has 4 options 1> "unsafe-none" 2> "same-origin-allow-popups" 3> "same-origin" 4> "noopener-allow-popups"')
        else:
            if self.Option not in Policies:
                raise SyntaxError('Cross-Origin-Opener-Policy has 4 options 1> "unsafe-none" 2> "same-origin-allow-popups" 3> "same-origin" 4> "noopener-allow-popups"')

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

        async def set_Cross_Origin_Opener_Policy(message: Message):
            """
            Sets the Cross-Origin-Opener-Policy header in the HTTP response headers.
            
            Args:
                message (dict): The message object representing the HTTP response.
            
            Returns:
                None

            """
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('Cross-Origin-Opener-Policy', self.Option if isinstance(self.Option, str) else self.Option['Cross-Origin-Opener-Policy'])

            await send(message)

        await self.app(scope, receive, set_Cross_Origin_Opener_Policy)