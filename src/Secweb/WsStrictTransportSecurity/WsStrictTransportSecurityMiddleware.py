'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2026, Motagamwala Taha Arif Ali '''

from typing import TypedDict
from starlette.datastructures import MutableHeaders
from starlette.types import Send, Receive, Scope, Message, ASGIApp

WsHSTSOptions = TypedDict(
    'WsHSTSOptions',
    {
        'max-age': int,
        'includeSubDomains': bool,
        'preload': bool
    },
    total=False
)

class WsHSTS:
    ''' HSTS class sets Strict-Transport-Security Header for Websocket.

    Example :
        app.add_middleware(WsHSTS, Option={})

    Parameter :
        Option (WsHSTSOptions, optional):
            - max-age (int): The maximum age of the Strict-Transport-Security header in seconds. (Default: 31536000)
            - includeSubDomains (bool): Whether to include subdomains in the Strict-Transport-Security header. (Default: True)
            - preload (bool): Whether to preload the Strict-Transport-Security header. (Default: False)
    
    '''
    def __init__(self, app: ASGIApp, Option: WsHSTSOptions = {'max-age': 31536000, 'includeSubDomains': True, 'preload': False}):
        """
        Initializes an instance of the class.

        Args:
            app (ASGIApp): The application object.
            Option (WsHSTSOptions, optional):
                - max-age (int): The maximum age of the Strict-Transport-Security header in seconds. (Default: 31536000)
                - includeSubDomains (bool): Whether to include subdomains in the Strict-Transport-Security header. (Default: True)
                - preload (bool): Whether to preload the Strict-Transport-Security header. (Default: False)

        Raises:
            SyntaxError: If 'max-age' is not a positive integer or if the 'Option' is not valid.

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

            
            if 'includeSubDomains' in Option and Option['includeSubDomains'] is not False:
                self.PolicyString += '; includeSubDomains'

            if 'preload' in Option and Option['preload'] is True:
                self.PolicyString += '; preload'     

        else:
            raise SyntaxError('Strict-Transport-Security has 3 options 1> "max-age=<expire-time>" <- This is the compulsory option 2> "includeSubDomains" 3> "preload"')

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """
        Asynchronously handles Websocket requests by routing them to the appropriate handler based on the request path.

        Parameters:
            scope (Scope): The scope of the request.
            receive (Receive): A function that returns a coroutine that reads messages from the server.
            send (Send): A function that sends messages to the server.
        """
        if scope["type"] != "websocket":
            return await self.app(scope, receive, send)

        async def set_Strict_Transport_Security(message: Message):  
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