'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2025, Motagamwala Taha Arif Ali '''

from starlette.datastructures import MutableHeaders

class WsHSTS:
    ''' HSTS class sets Strict-Transport-Security Header for Websocket.

    Example :
        app.add_middleware(WsHSTS, Option={})

    Parameter :
        Option (dict, optional): The options for the class. Defaults to {'max-age': 432000, 'includeSubDomains': True, 'preload': False}.
    
    '''
    def __init__(self, app, Option = {'max-age': 432000, 'includeSubDomains': True, 'preload': False}):
        """
        Initializes an instance of the class.

        Args:
            app (object): The application object.
            Option (dict, optional): The options for the class. Defaults to {'max-age': 432000, 'includeSubDomains': True, 'preload': False}.

        Raises:
            SyntaxError: If 'max-age' is not a positive integer or if the 'Option' dictionary is not valid.

        Returns:
            None
        """
        self.app = app
        self.PolicyString = ''
        if 'max-age' in Option:
            if int(Option['max-age']) and Option['max-age'] > 0:
                self.PolicyString += 'max-age=' + str(Option['max-age'])
            else:
                raise SyntaxError('max-age needs to be a positive integer')

            try:
                if Option['includeSubDomains'] is not False:
                    self.PolicyString += '; includeSubDomains'
            except KeyError:
                self.PolicyString += '; includeSubDomains'

            if 'preload' in Option and Option['preload'] is True:
                self.PolicyString += '; preload'     

        else:
            raise SyntaxError('Strict-Transport-Security has 3 options 1> "max-age=<expire-time>" <- This is the compulsory option 2> "includeSubDomains" 3> "preload"')

    async def __call__(self, scope, receive, send):
        """
        Asynchronously handles Websocket requests by routing them to the appropriate handler based on the request path.

        Parameters:
            scope (Dict[str, Any]): The scope of the request.
            receive (Callable[[], Awaitable[Dict[str, Any]]]): A function that returns a coroutine that reads messages from the server.
            send (Callable[[Dict[str, Any]], Awaitable[None]]): A function that sends messages to the server.
        """
        if scope["type"] != "websocket":
            return await self.app(scope, receive, send)

        async def set_Strict_Transport_Security(message):  
            """
            Set the Strict-Transport-Security header in the response headers if the message type is "websocket.accept".
            
            Args:
                message (dict): The message object containing information about the request.
            
            Returns:
                None

            """
            if message["type"] == "websocket.accept":
                headers = MutableHeaders(scope=message) 
                headers.append('Strict-Transport-Security', self.PolicyString)

            await send(message)

        await self.app(scope, receive, set_Strict_Transport_Security)