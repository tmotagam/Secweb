'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2025, Motagamwala Taha Arif Ali '''

from warnings import warn
from starlette.datastructures import MutableHeaders

class XFrame:
    ''' XFrame class sets X-Frame-Options header.

    Example:
        app.add_middleware(XFrame, Option='')

    Parameter:
        Option (str, optional): Option for the function. Defaults to 'DENY'.

    '''
    def __init__(self, app, Option = 'DENY'):
        """
        Initializes a new instance of the class.

        Args:
            app (object): The app object.
            Option (str, optional): Option for the function. Defaults to 'DENY'.

        Raises:
            SyntaxError: If the value of the Option is not 'SAMEORIGIN' or 'DENY'.

        Returns:
            None
        """
        self.app = app
        self.Option = Option
        if not isinstance(self.Option, str):
            warn('XFrame middleware will now accept string rather than dictonary eg. Option={"X-Frame-Options": "DENY"} will be Option="DENY"', SyntaxWarning, 2)
            if self.Option['X-Frame-Options'] != 'SAMEORIGIN' and self.Option['X-Frame-Options'] != 'DENY':
                raise SyntaxError('X-Frame-Options has two values only 1> "DENY" 2> "SAMEORIGIN"')
        else:
            if self.Option != 'SAMEORIGIN' and self.Option != 'DENY':
                raise SyntaxError('XFrame has two values only 1> "DENY" 2> "SAMEORIGIN"') 

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

        async def set_x_Frame_Options(message):
            """
            Sets the 'X-Frame-Options' header in the response header.

            Args:
                message (dict): The message received from the server.

            Returns:
                None
            """
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('X-Frame-Options', self.Option if isinstance(self.Option, str) else self.Option['X-Frame-Options'])

            await send(message)

        await self.app(scope, receive, set_x_Frame_Options)