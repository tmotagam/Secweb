'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2023, Motagamwala Taha Arif Ali '''

from warnings import warn
from starlette.types import Scope, Receive, Send, ASGIApp, Message
from starlette.datastructures import MutableHeaders

class ExpectCt:
    ''' ExpectCt class takes only one parameter Option for setting the Expect-CT header (deprecated)

    Example :
        app.add_middleware(ExpectCt, Option={})

    Parameter :

    Option={} This is a dictionary'''
    def __init__(self, app: ASGIApp, Option: dict[str, str | bool | int] = {'max-age': 123, 'enforce': False, 'report-uri': ''}):
        self.app = app
        self.PolicyString = ''
        warn("Expect-CT Header is now deprecated by browsers and may be removed from the library in the upcoming versions", SyntaxWarning, 2)
        if 'max-age' in Option:
            if int(Option['max-age']) and int(Option['max-age']) > 0:
                self.PolicyString += 'max-age=' + str(Option['max-age'])
            else:
                raise SyntaxError('max-age needs to be a positive integer')

            if 'enforce' in Option and Option['enforce'] is True:
                self.PolicyString += ', enforce'

            if 'report-uri' in Option and Option['report-uri'] != '':
                self.PolicyString += ', report-uri=' + '"' + str(Option['report-uri']) + '"'

        else:
            raise SyntaxError('Expect-CT has 3 options 1> "max-age=<Age>" <- This is the compulsory option 2> "enforce" 3> "report-uri=<Your URI>"')

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_Expect_CT(message: Message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('Expect-CT', self.PolicyString)

            await send(message)

        await self.app(scope, receive, set_Expect_CT)