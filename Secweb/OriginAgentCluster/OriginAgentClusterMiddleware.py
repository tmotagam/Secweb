'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2023, Motagamwala Taha Arif Ali '''

from starlette.datastructures import MutableHeaders

class OriginAgentCluster:
    ''' OriginAgentCluster sets the Origin-Agent-Cluster header it takes no parameter

    Example :
        app.add_middleware(OriginAgentCluster)'''
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_Origin_Agent_Cluster(message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('Origin-Agent-Cluster', '?1')

            await send(message)

        await self.app(scope, receive, set_Origin_Agent_Cluster)