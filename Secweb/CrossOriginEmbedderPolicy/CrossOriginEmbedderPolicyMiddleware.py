'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2024, Motagamwala Taha Arif Ali '''

from starlette.datastructures import MutableHeaders

class CrossOriginEmbedderPolicy:
    ''' CrossOriginEmbedderPolicy class sets Cross-Origin-Embedder-Policy header.

    Example:
        app.add_middleware(CrossOriginEmbedderPolicy, Option={})

    Parameter:
        Option: The options for the class. Defaults to {'Cross-Origin-Embedder-Policy': 'unsafe-none'}.
    
    '''
    def __init__(self, app, Option = {'Cross-Origin-Embedder-Policy': 'unsafe-none'}):
        """
        Initializes the class with the given `app` and `Option` parameters.

        Args:
            app: The app object.
            Option: The options for the class. Defaults to {'Cross-Origin-Embedder-Policy': 'unsafe-none'}.

        Raises:
            SyntaxError: If the `Cross-Origin-Embedder-Policy` option is not one of the valid options:
                         'require-corp', 'unsafe-none', 'credentialless'.
        """
        self.app = app
        self.Option = Option
        Policies = ['require-corp', 'unsafe-none', 'credentialless']
        if self.Option['Cross-Origin-Embedder-Policy'] not in Policies:
            raise SyntaxError('Cross-Origin-Embedder-Policy has 3 options 1> "unsafe-none" 2> "require-corp" 3> "credentialless"')

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

        async def set_Cross_Origin_Embedder_Policy(message):
            """
            Set the Cross-Origin-Embedder-Policy header in the response headers.
            
            :param message: The message containing the response headers.
            """
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('Cross-Origin-Embedder-Policy', self.Option['Cross-Origin-Embedder-Policy'])

            await send(message)

        await self.app(scope, receive, set_Cross_Origin_Embedder_Policy)