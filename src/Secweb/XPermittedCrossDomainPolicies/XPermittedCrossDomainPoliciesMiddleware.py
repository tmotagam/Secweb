'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2026, Motagamwala Taha Arif Ali '''

from typing import Literal, Union
from warnings import warn
from starlette.datastructures import MutableHeaders
from starlette.types import Send, Receive, Scope, Message, ASGIApp

XPermittedCrossDomainPoliciesLiteral = Literal['none', 'master-only', 'by-content-type', 'all']

XPermittedCrossDomainPoliciesOptions = Union[dict[Literal['X-Permitted-Cross-Domain-Policies'], XPermittedCrossDomainPoliciesLiteral], XPermittedCrossDomainPoliciesLiteral]

class XPermittedCrossDomainPolicies:
    ''' XPermittedCrossDomainPolicies class sets X-Permitted-Cross-Domain-Policies header.

    Example:
        app.add_middleware(XPermittedCrossDomainPolicies, Option='')

    Parameter:
        Option (XPermittedCrossDomainPoliciesOptions, optional): cross-domain policy options. Default is 'none'.

    '''
    def __init__(self, app: ASGIApp, Option: XPermittedCrossDomainPoliciesOptions = 'none'):
        """
        Initializes the class with the given app and optional cross-domain policy option.

        Parameters:
            app (ASGIApp): The app object.
            Option (XPermittedCrossDomainPoliciesOptions, optional): cross-domain policy options. Default is 'none'.

        Raises:
            SyntaxError: If the value of the Option is not one of the valid policies.

        Returns:
            None
        """
        self.app = app
        self.Option = Option
        Policies = ['none', 'master-only', 'by-content-type', 'all']
        if not isinstance(self.Option, str):
            warn('XPermittedCrossDomainPolicies middleware will now accept string rather than dictonary eg. Option={"X-Permitted-Cross-Domain-Policies": "none"} will be Option="none"', SyntaxWarning, 2)
            if self.Option['X-Permitted-Cross-Domain-Policies'] not in Policies:
                raise SyntaxError('X-Permitted-Cross-Domain-Policies has four values 1> "none" 2> "master-only" 3> "by-content-type" 4> "all"')
        else:
            if self.Option not in Policies:
                raise SyntaxError('XPermittedCrossDomainPolicies has four values 1> "none" 2> "master-only" 3> "by-content-type" 4> "all"') 

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

        async def set_x_Permitted_Cross_Domain_Policies(message: Message):
            """
            Set the X-Permitted-Cross-Domain-Policies header in the response headers.

            Args:
                message (dict): The message containing the type and scope of the response.

            Returns:
                None
            """
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('X-Permitted-Cross-Domain-Policies', self.Option if isinstance(self.Option, str) else self.Option['X-Permitted-Cross-Domain-Policies'])

            await send(message)

        await self.app(scope, receive, set_x_Permitted_Cross_Domain_Policies)