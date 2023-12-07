'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2024, Motagamwala Taha Arif Ali '''

from starlette.datastructures import MutableHeaders

class XDNSPrefetchControl:
    ''' XDNSPrefetchControl class sets X-DNS-Prefetch-Control header.

    Example:
        app.add_middleware(XDNSPrefetchControl, Option={})

    Parameter:
        Option (dict): Optional. The options for the class object. Defaults to {'X-DNS-Prefetch-Control': 'off'}.
    
    '''
    def __init__(self, app, Option = {'X-DNS-Prefetch-Control': 'off'}):
        """
        Initializes the class object.

        Parameters:
            app (object): The application object.
            Option (dict): Optional. The options for the class object. Defaults to {'X-DNS-Prefetch-Control': 'off'}.

        Raises:
            SyntaxError: If the value of Option['X-DNS-Prefetch-Control'] is neither 'on' nor 'off'.
        """
        self.app = app
        self.Option = Option
        if self.Option['X-DNS-Prefetch-Control'] != 'on' and self.Option['X-DNS-Prefetch-Control'] != 'off':
            raise SyntaxError('X-DNS-Prefetch-Control has two values only 1> "on" 2> "off"')

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

        async def set_x_DNS_Prefetch_Control(message):
            """
            Sets the value of the `X-DNS-Prefetch-Control` header in the response headers.

            Parameters:
                message (dict): The message object received from the server.

            Returns:
                None
            """
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('X-DNS-Prefetch-Control', self.Option['X-DNS-Prefetch-Control'])

            await send(message)

        await self.app(scope, receive, set_x_DNS_Prefetch_Control)