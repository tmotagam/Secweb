'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2024, Motagamwala Taha Arif Ali '''

from warnings import warn
from starlette.datastructures import MutableHeaders

class PermissionsPolicy:
    '''PermissionsPolicy class sets Permissions-Policy header.

    Example :
        app.add_middleware(PermissionsPolicy, Option={})

    Parameters :
       Option (dict): The options for the permission policy.
    
    '''
    def __init__(self, app, Option = {}):
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
        Policy = ["accelerometer", "ambient-light-sensor", "attribution-reporting", "autoplay", "battery", "browsing-topics", "camera", "display-capture", "document-domain", "encrypted-media", "execution-while-not-rendered", "execution-while-out-of-viewport", "fullscreen", "gamepad", "geolocation", "gyroscope", "hid", "identity-credentials-get", "idle-detection", "local-fonts", "magnetometer", "microphone", "midi", "otp-credentials", "payment", "picture-in-picture", "publickey-credentials-create", "publickey-credentials-get", "screen-wake-lock", "serial", "speaker-selection", "storage-access", "usb", "web-share", "window-management", "xr-spatial-tracking"]
        if Option == {}:
            raise SyntaxError('Option cannot be empty for Permission-Policy to be applied')
        else:
            warn("Permission-Policy header is still under working draft, browsers might give warnings and errors", SyntaxWarning, 2)
            self.__PolicyCheck__(Option, Policy)
    
    def __PolicyCheck__(self, Option, Policy):
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

        async def set_Permissions_Policy(message):
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
