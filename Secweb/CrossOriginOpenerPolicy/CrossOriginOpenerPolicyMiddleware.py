'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2024, Motagamwala Taha Arif Ali '''

from starlette.datastructures import MutableHeaders

class CrossOriginOpenerPolicy:
    ''' CrossOriginOpenerPolicy class sets Cross-Origin-Opener-Policy header.

    Example:
        app.add_middleware(CrossOriginOpenerPolicy, Option={})

    Parameter:
        Option (dict): The options for the class. Defaults to {'Cross-Origin-Opener-Policy': 'unsafe-none'}.
    
    '''
    def __init__(self, app, Option = {'Cross-Origin-Opener-Policy': 'unsafe-none'}):
        """
        Initializes an instance of the class.

        Args:
            app (object): The app object.
            Option (dict): The options for the class. Defaults to {'Cross-Origin-Opener-Policy': 'unsafe-none'}.

        Raises:
            SyntaxError: If the value of Option['Cross-Origin-Opener-Policy'] is not one of the allowed policies.

        Returns:
            None
        """
        self.app = app
        self.Option = Option
        Policies = ['unsafe-none', 'same-origin-allow-popups', 'same-origin']
        if self.Option['Cross-Origin-Opener-Policy'] not in Policies:
            raise SyntaxError('Cross-Origin-Opener-Policy has 3 options 1> "unsafe-none" 2> "same-origin-allow-popups" 3> "same-origin"')

    async def __call__(self, scope, receive, send):
        """
        Asynchronously handles HTTP requests by routing them to the appropriate handler based on the request path.

        Parameters:
            scope (Dict[str, Any]): The scope of the request.
            receive (Callable[[], Awaitable[Dict[str, Any]]]): A function that returns a coroutine that reads messages from the server.
            send (Callable[[Dict[str, Any]], Awaitable[None]]): A function that sends messages to the server.

        Returns:
            None
        """
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_Cross_Origin_Opener_Policy(message):
            """
            Sets the Cross-Origin-Opener-Policy header in the HTTP response headers.
            
            Args:
                message (dict): The message object representing the HTTP response.
            
            Returns:
                None

            """
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('Cross-Origin-Opener-Policy', self.Option['Cross-Origin-Opener-Policy'])

            await send(message)

        await self.app(scope, receive, set_Cross_Origin_Opener_Policy)