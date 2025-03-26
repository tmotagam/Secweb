'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2025, Motagamwala Taha Arif Ali '''
from typing import TypedDict
from warnings import warn

from starlette.applications import Starlette
from starlette.datastructures import MutableHeaders
from starlette.types import Message, Scope, Receive, Send

PermissionsPolicyOption = TypedDict(
    "PermissionsPolicyOption",
    {
        "accelerometer": list[str],
        "ambient-light-sensor": list[str],
        "attribution-reporting": list[str],
        "autoplay": list[str],
        "bluetooth": list[str],
        "browsing-topics": list[str],
        "camera": list[str],
        "compute-pressure": list[str],
        "display-capture": list[str],
        "document-domain": list[str],
        "encrypted-media": list[str],
        "fullscreen": list[str],
        "geolocation": list[str],
        "gyroscope": list[str],
        "hid": list[str],
        "identity-credentials-get": list[str],
        "idle-detection": list[str],
        "local-fonts": list[str],
        "magnetometer": list[str],
        "microphone": list[str],
        "midi": list[str],
        "otp-credentials": list[str],
        "payment": list[str],
        "picture-in-picture": list[str],
        "publickey-credentials-create": list[str],
        "publickey-credentials-get": list[str],
        "screen-wake-lock": list[str],
        "serial": list[str],
        "storage-access": list[str],
        "usb": list[str],
        "web-share": list[str],
        'window-management':list[str]
    },
    total=False,

)



class PermissionsPolicy:
    '''PermissionsPolicy class sets Permissions-Policy header.

    Example :
        app.add_middleware(PermissionsPolicy, Option={})

    Parameters :
       Option (dict): The options for the permission policy.
    
    '''
    def __init__(self, app: Starlette, Option: PermissionsPolicyOption = {}):
        """
        Initializes a new instance of the class.

        Parameters:
            app (object): The application object.
            Option (dict): The options for the permission policy.

        Raises:
            SyntaxError: If the `Option` parameter is empty.

        Warnings:
            SyntaxWarning: The `Permission-Policy` header is still under working draft, browsers might give warnings and errors.

        Returns:
            None
        """
        self.app = app
        self.PolicyString = ''
        Policy = ["accelerometer", "ambient-light-sensor", "attribution-reporting", "autoplay", "bluetooth", "browsing-topics", "camera", "compute-pressure", "display-capture", "document-domain", "encrypted-media", "fullscreen", "geolocation", "gyroscope", "hid", "identity-credentials-get", "idle-detection", "local-fonts", "magnetometer", "microphone", "midi", "otp-credentials", "payment", "picture-in-picture", "publickey-credentials-create", "publickey-credentials-get", "screen-wake-lock", "serial", "storage-access", "usb", "web-share", "window-management", "xr-spatial-tracking"]
        if Option == {}:
            raise SyntaxError('Option cannot be empty for Permission-Policy to be applied')
        else:
            warn("Permission-Policy header is still under working draft, browsers might give warnings and errors", SyntaxWarning, 2)
            self.__PolicyCheck__(Option, Policy)
    
    def __PolicyCheck__(self, Option: PermissionsPolicyOption, Policy: list[str]) -> None:
        """
        Generate a policy string based on the given Option and Policy dictionaries.

        Args:
            Option (dict): The Option dictionary.
            Policy (dict): The Policy dictionary.

        Raises:
            SyntaxError: If a key in Option is not present in Policy.
            SyntaxError: If an allowlist item is invalid.

        Returns:
            None
        """
        keys = list(Option.keys())

        for i, key in enumerate(keys):
            if key not in Policy:
                raise SyntaxError(f'The Policy { key } does not exist')

            self.PolicyString += key
            values = Option[key]

            if i == len(keys) - 1:
                if len(values) != 0:
                    self.PolicyString += "=("
                else:
                    self.PolicyString += '=()'
            elif len(values) == 0:
                self.PolicyString += '=(), '
                continue
            else:
                self.PolicyString += "=("

            for j, value in enumerate(values):
                if value != 'self' and value != '*':
                    if value[0] != '"':
                        raise SyntaxError(f'Invalid allowlist item({ value }) for feature { key }. Allowlist item must be *, self, src or a quoted URL "https://example.com"')

                self.PolicyString += value

                if j == len(values) - 1:
                    if i == len(keys) - 1:
                        self.PolicyString += ')'
                    else:
                        self.PolicyString += '), '
                else:
                    self.PolicyString += ' '

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
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

        async def set_Permissions_Policy(message: Message) -> None:
            """
            Set the Permissions-Policy header in the HTTP response headers.

            Parameters:
                message (dict): The message object representing the HTTP response.

            Returns:
                None
            """
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('Permissions-Policy', self.PolicyString)

            await send(message)

        await self.app(scope, receive, set_Permissions_Policy)
