'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2026, Motagamwala Taha Arif Ali '''

from typing import Literal, Union
from warnings import warn
from starlette.types import Send, Receive, Scope, Message, ASGIApp

from starlette.datastructures import MutableHeaders

CrossOriginResourcePolicyLiteral = Literal['same-site', 'same-origin', 'cross-origin']

CrossOriginResourcePolicyOptions = Union[dict[Literal['Cross-Origin-Resource-Policy'], CrossOriginResourcePolicyLiteral], CrossOriginResourcePolicyLiteral]

class CrossOriginResourcePolicy:
    ''' CrossOriginResourcePolicy class sets Cross-Origin-Resource-Policy header.

    Example:
        app.add_middleware(CrossOriginResourcePolicy, Option='')

    Parameter:
        Option (CrossOriginResourcePolicyOptions, optional):
            - 'same-site': Sets the Cross-Origin-Resource-Policy header to 'same-site'. (Default)
            - 'same-origin': Sets the Cross-Origin-Resource-Policy header to 'same-origin'.
            - 'cross-origin': Sets the Cross-Origin-Resource-Policy header to 'cross-origin'.
        
    '''
    def __init__(self, app: ASGIApp, Option: CrossOriginResourcePolicyOptions = 'cross-origin'):
        """
        Initializes an instance of the class.

        Parameters:
            app (ASGIApp): The app object.
            Option (CrossOriginResourcePolicyOptions, optional):
                - 'same-site': Sets the Cross-Origin-Resource-Policy header to 'same-site'. (Default)
                - 'same-origin': Sets the Cross-Origin-Resource-Policy header to 'same-origin'.
                - 'cross-origin': Sets the Cross-Origin-Resource-Policy header to 'cross-origin'.

        Raises:
            SyntaxError: If the 'CrossOriginResourcePolicy' Option is not one of the allowed policies.

        Returns:
            None
        """
        self.app = app
        self.Option = Option
        Policies = ['same-site', 'same-origin', 'cross-origin']
        if not isinstance(self.Option, str):
            warn('CrossOriginResourcePolicy middleware will now accept string rather than dictonary eg. Option={"Cross-Origin-Resource-Policy": "cross-origin"} will be Option="cross-origin"', SyntaxWarning, 2)
            if self.Option['Cross-Origin-Resource-Policy'] not in Policies:
                raise SyntaxError('Cross-Origin-Resource-Policy has 3 options 1> "same-site" 2> "same-origin" 3> "cross-origin"')
        else:
            if self.Option not in Policies:
                raise SyntaxError('CrossOriginResourcePolicy has 3 options 1> "same-site" 2> "same-origin" 3> "cross-origin"')

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

        async def set_Cross_Origin_Resource_Policy(message: Message):
            """
            Sets the Cross-Origin Resource Policy header in the response headers.

            Parameters:
                message (dict): The message containing the type and scope of the response.

            Returns:
                None

            """
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('Cross-Origin-Resource-Policy', self.Option if isinstance(self.Option, str) else self.Option['Cross-Origin-Resource-Policy'])

            await send(message)

        await self.app(scope, receive, set_Cross_Origin_Resource_Policy)