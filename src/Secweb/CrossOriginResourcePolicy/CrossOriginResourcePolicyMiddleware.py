'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2025, Motagamwala Taha Arif Ali '''

from warnings import warn
from starlette.datastructures import MutableHeaders

class CrossOriginResourcePolicy:
    ''' CrossOriginResourcePolicy class sets Cross-Origin-Resource-Policy header.

    Example:
        app.add_middleware(CrossOriginResourcePolicy, Option='')

    Parameter:
        Option (str): The option for the class. Default is 'cross-origin'.
        
    '''
    def __init__(self, app, Option = 'cross-origin'):
        """
        Initializes an instance of the class.

        Parameters:
            app (object): The app object.
            Option (str): The option for the class. Default is 'cross-origin'.

        Raises:
            SyntaxError: If the 'CrossOriginResourcePolicy' Option is not one of 'same-site', 'same-origin', 'cross-origin'.

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

        async def set_Cross_Origin_Resource_Policy(message):
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