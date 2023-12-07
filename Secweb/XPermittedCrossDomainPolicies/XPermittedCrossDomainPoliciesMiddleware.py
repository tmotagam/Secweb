'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2024, Motagamwala Taha Arif Ali '''

from starlette.datastructures import MutableHeaders

class XPermittedCrossDomainPolicies:
    ''' XPermittedCrossDomainPolicies class sets X-Permitted-Cross-Domain-Policies header.

    Example:
        app.add_middleware(XPermittedCrossDomainPolicies, Option={})

    Parameter:
        Option (dict): Optional cross-domain policy option. Default is {'X-Permitted-Cross-Domain-Policies': 'none'}.

    '''
    def __init__(self, app, Option = {'X-Permitted-Cross-Domain-Policies': 'none'}):
        """
        Initializes the class with the given app and optional cross-domain policy option.

        Parameters:
            app (object): The app object.
            Option (dict): Optional cross-domain policy option. Default is {'X-Permitted-Cross-Domain-Policies': 'none'}.

        Raises:
            SyntaxError: If the value of Option['X-Permitted-Cross-Domain-Policies'] is not one of the valid policies.

        Returns:
            None
        """
        self.app = app
        self.Option = Option
        Policies = ['none', 'master-only', 'by-content-type', 'all']
        if self.Option['X-Permitted-Cross-Domain-Policies'] not in Policies:
            raise SyntaxError('X-Permitted-Cross-Domain-Policies has four values 1> "none" 2> "master-only" 3> "by-content-type" 4> "all"')

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

        async def set_x_Permitted_Cross_Domain_Policies(message):
            """
            Set the X-Permitted-Cross-Domain-Policies header in the response headers.

            Args:
                message (dict): The message containing the type and scope of the response.

            Returns:
                None
            """
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('X-Permitted-Cross-Domain-Policies', self.Option['X-Permitted-Cross-Domain-Policies'])

            await send(message)

        await self.app(scope, receive, set_x_Permitted_Cross_Domain_Policies)