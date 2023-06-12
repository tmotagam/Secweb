'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2023, Motagamwala Taha Arif Ali '''

from starlette.types import Scope, Receive, Send, ASGIApp, Message
from starlette.datastructures import MutableHeaders

class HSTS:
    ''' HSTS class sets Strict-Transport-Security Header it takes one parameter

    Example :
        app.add_middleware(HSTS, Option={})

    Parameter :

    Option={} This is a dictionary'''
    def __init__(self, app: ASGIApp, Option: dict[str, int | bool] = {'max-age': 432000, 'includeSubDomains': True, 'preload': False}):
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

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_Strict_Transport_Security(message: Message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message) 
                headers.append('Strict-Transport-Security', self.PolicyString)

            await send(message)

        await self.app(scope, receive, set_Strict_Transport_Security)