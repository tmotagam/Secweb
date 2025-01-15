'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2025, Motagamwala Taha Arif Ali '''

from starlette.datastructures import MutableHeaders
from starlette.convertors import CONVERTOR_TYPES
from re import compile, escape

def __path_regex_builder__(path):
    """
    Generate a regular expression pattern for a given path.

    Args:
        path (str): The path to generate the regular expression pattern for.

    Returns:
        re.Pattern: The compiled regular expression pattern.

    Raises:
        ValueError: If there are duplicated parameter names in the path.
        AssertionError: If an unknown path convertor is encountered.
    """
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
    ''' ClearSiteData class sets Clear-Site-Data header.

    Example:
        app.add_middleware(ClearSiteData, Option={}, Routes=[])

    Parameter:
        Option (dict, optional): The options for the class. Defaults to {'cache': True, 'cookies': True, 'storage': True}.
        Routes (list, optional): The list of routes. Defaults to [].
    
    '''
    def __init__(self, app, Option = {'cache': True, 'cookies': True, 'storage': True}, Routes = []):
        """
        Initializes the class with the provided parameters.

        Args:
            app (object): The application object.
            Option (dict, optional): The options for the class. Defaults to {'cache': True, 'cookies': True, 'storage': True}.
            Routes (list, optional): The list of routes. Defaults to [].

        Raises:
            SyntaxError: If the routes are empty.

        Returns:
            None
        """
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
        
        async def set_route(message):
            """
            Sets the header for the given route.

            Args:
                message (dict): The message object containing the type and other information.

            Returns:
                None
            """
            if message["type"] == "http.response.start":
                for i in self.pathregex:
                    if i.match(scope["path"]):
                        headers = MutableHeaders(scope=message)
                        headers.append('Clear-Site-Data', self.policyString)
                        break

            await send(message)

        await self.app(scope, receive, set_route)