'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2025, Motagamwala Taha Arif Ali '''

from warnings import warn
from starlette.datastructures import MutableHeaders

class ReferrerPolicy:
    ''' ReferrerPolicy class sets Referrer-Policy header.

    Example:
        app.add_middleware(ReferrerPolicy, Option=[])

    Parameter:
        Option (list[str], optional): The `Option` parameter is a list of string that contains the option for the `Referrer-Policy`. The default value is ['strict-origin-when-cross-origin'].
    
    '''
    def __init__(self, app, Option = ['strict-origin-when-cross-origin']):
        """
        Initializes the class with the given `app` and `Option` parameters.

        Parameters:
            app (object): The `app` parameter is the application object.
            Option (list[str], optional): The `Option` parameter is a list of string that contains the option for the `Referrer-Policy`. The default value is ['strict-origin-when-cross-origin'].

        Raises:
            SyntaxError: If the `Referrer-Policy` option is not one of the valid options.

        Returns:
            None
        """
        self.app = app
        Policies = ['no-referrer', 'no-referrer-when-downgrade', 'origin', 'origin-when-cross-origin', 'same-origin', 'strict-origin', 'strict-origin-when-cross-origin', 'unsafe-url']
        self.policystring = ''
        if not isinstance(Option, list):
            warn('ReferrerPolicy middleware will now accept list of string(s) rather than dictonary eg. Option={"Referrer-Policy": "strict-origin-when-cross-origin"} will be Option=["strict-origin-when-cross-origin"]', SyntaxWarning, 2)
            if Option['Referrer-Policy'] in Policies:
                self.policystring = Option['Referrer-Policy']
            elif len(Option['Referrer-Policy']) > 1:
                for option in Option['Referrer-Policy']:
                    if option not in Policies:
                        raise SyntaxError('Referrer-Policy has 8 options 1> "no-referrer" 2> "no-referrer-when-downgrade" 3> "origin" 4> "origin-when-cross-origin" 5> "same-origin" 6> "strict-origin" 7> "strict-origin-when-cross-origin" 8> "unsafe-url"')
                self.policystring = ', '.join(Option['Referrer-Policy'])
            else:
                raise SyntaxError('Referrer-Policy has 8 options 1> "no-referrer" 2> "no-referrer-when-downgrade" 3> "origin" 4> "origin-when-cross-origin" 5> "same-origin" 6> "strict-origin" 7> "strict-origin-when-cross-origin" 8> "unsafe-url"')
        else:
            for option in Option:
                if option not in Policies:
                    raise SyntaxError('ReferrerPolicy has 8 options 1> "no-referrer" 2> "no-referrer-when-downgrade" 3> "origin" 4> "origin-when-cross-origin" 5> "same-origin" 6> "strict-origin" 7> "strict-origin-when-cross-origin" 8> "unsafe-url"')
            self.policystring = ', '.join(Option)

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

        async def set_Referrer_Policy(message):
            """
            Set the Referrer-Policy header in the HTTP response.

            Parameters:
                message (dict): The message containing the type and scope of the response.

            Returns:
                None
            """
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('Referrer-Policy', self.policystring)

            await send(message)

        await self.app(scope, receive, set_Referrer_Policy)