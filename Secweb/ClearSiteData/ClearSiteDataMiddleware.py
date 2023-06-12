'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2023, Motagamwala Taha Arif Ali '''

from starlette.types import Scope, Receive, Send, ASGIApp, Message
from starlette.datastructures import MutableHeaders
from starlette.convertors import CONVERTOR_TYPES
from re import compile, escape

def __path_regex_builder__(path: str):
    is_host = not path.startswith("/")

    path_regex = "^"
    duplicated_params = set()

    idx = 0
    for match in compile("{([a-zA-Z_][a-zA-Z0-9_]*)(:[a-zA-Z_][a-zA-Z0-9_]*)?}").finditer(path):
        param_name, convertor_type = match.groups("str")
        convertor_type = convertor_type.lstrip(":")
        assert (
            convertor_type in CONVERTOR_TYPES
        ), f"Unknown path convertor '{convertor_type}'"
        convertor = CONVERTOR_TYPES[convertor_type]

        path_regex += escape(path[idx : match.start()])
        path_regex += f"(?P<{param_name}>{convertor.regex})"

        idx = match.end()

    if duplicated_params:
        names = ", ".join(sorted(duplicated_params))
        ending = "s" if len(duplicated_params) > 1 else ""
        raise ValueError(f"Duplicated param name{ending} {names} at path {path}")

    if is_host:
        hostname = path[idx:].split(":")[0]
        path_regex += escape(hostname) + "$"
    else:
        path_regex += escape(path[idx:]) + "$"

    return compile(path_regex)

class ClearSiteData:
    ''' ClearSiteData class sets Clear-Site-Data header it takes two Parameter

    Example:
        app.add_middleware(ClearSiteData, Option={}, Routes=[])

    Parameter:

    Option={} This is a dictionary

    Routes=[] This is an Array'''
    def __init__(self, app: ASGIApp, Option: dict[str, bool] = {'cache': True, 'cookies': True, 'storage': True}, Routes: list[str] = []):
        self.app = app
        self.policyString = ''
        if Routes.__len__() == 0:
            raise SyntaxError('Cannot Set Clear-Site-Data header if the routes are empty')
        
        self.pathregex = [__path_regex_builder__(i) for i in Routes]

        if '*' in Option and Option['*'] is True:
            self.policyString += '"*"'
            Option.pop('*')
        else:
            if 'cache' in Option and Option['cache'] is True:
                self.policyString += '"cache"' if list(Option.keys()).__len__() == 1 else '"cache", '
                Option.pop('cache')
            if 'cookies' in Option and Option['cookies'] is True:
                self.policyString += '"cookies"' if list(Option.keys()).__len__() == 1 else '"cookies", '
                Option.pop('cookies')
            if 'storage' in Option and Option['storage'] is True:
                self.policyString += '"storage"'
                Option.pop('storage')

        if list(Option.keys()).__len__() != 0 :
            raise SyntaxError('Clear-Site-Data has 4 options 1> "cache" 2> "cookies" 3> "storage" 4> "*"')

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        
        async def set_route(message: Message):
            if message["type"] == "http.response.start":
                for i in self.pathregex:
                    if i.match(scope["path"]):
                        headers = MutableHeaders(scope=message)
                        headers.append('Clear-Site-Data', self.policyString)
                        break

            await send(message)

        await self.app(scope, receive, set_route)