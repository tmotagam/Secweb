'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2023, Motagamwala Taha Arif Ali '''

from starlette.types import Scope, Receive, Send, ASGIApp, Message
from starlette.datastructures import MutableHeaders

class XPermittedCrossDomainPolicies:
    ''' XPermittedCrossDomainPolicies class sets X-Permitted-Cross-Domain-Policies header it takes one Parameter

    Example:
        app.add_middleware(XPermittedCrossDomainPolicies, Option={})

    Parameter:

    Option={} This is a dictionary'''
    def __init__(self, app: ASGIApp, Option: dict[str, str] = {'X-Permitted-Cross-Domain-Policies': 'none'}):
        self.app = app
        self.Option = Option
        Policies = ['none', 'master-only', 'by-content-type', 'all']
        if self.Option['X-Permitted-Cross-Domain-Policies'] not in Policies:
            raise SyntaxError('X-Permitted-Cross-Domain-Policies has four values 1> "none" 2> "master-only" 3> "by-content-type" 4> "all"')

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_x_Permitted_Cross_Domain_Policies(message: Message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('X-Permitted-Cross-Domain-Policies', self.Option['X-Permitted-Cross-Domain-Policies'])

            await send(message)

        await self.app(scope, receive, set_x_Permitted_Cross_Domain_Policies)