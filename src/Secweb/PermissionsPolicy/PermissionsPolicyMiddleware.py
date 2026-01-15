'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2026, Motagamwala Taha Arif Ali '''

from typing import List, Literal, TypedDict, Union
from warnings import warn
from starlette.datastructures import MutableHeaders
from starlette.types import Send, Receive, Scope, Message, ASGIApp

OptionValues = List[Union[Literal["self"], Literal["*"], str]]

PermissionsPolicyOptions = TypedDict(
    'PermissionsPolicyOptions',
    {
        "accelerometer": OptionValues,
        "ambient-light-sensor": OptionValues,
        "aria-notify": OptionValues,
        "attribution-reporting": OptionValues,
        "autoplay": OptionValues,
        "bluetooth": OptionValues,
        "browsing-topics": OptionValues,
        "camera": OptionValues,
        "captured-surface-control": OptionValues,
        "compute-pressure": OptionValues,
        "cross-origin-isolated": OptionValues,
        "deferred-fetch": OptionValues,
        "deferred-fetch-minimal": OptionValues,
        "display-capture": OptionValues,
        "encrypted-media": OptionValues,
        "fullscreen": OptionValues,
        "geolocation": OptionValues,
        "gyroscope": OptionValues,
        "hid": OptionValues,
        "identity-credentials-get": OptionValues,
        "idle-detection": OptionValues,
        "local-fonts": OptionValues,
        "magnetometer": OptionValues,
        "microphone": OptionValues,
        "midi": OptionValues,
        "on-device-speech-recognition": OptionValues,
        "otp-credentials": OptionValues,
        "payment": OptionValues,
        "picture-in-picture": OptionValues,
        "private-state-token-issuance": OptionValues,
        "private-state-token-redemption": OptionValues,
        "publickey-credentials-create": OptionValues,
        "publickey-credentials-get": OptionValues,
        "screen-wake-lock": OptionValues,
        "serial": OptionValues,
        "storage-access": OptionValues,
        "summarizer": OptionValues,
        "usb": OptionValues,
        "web-share": OptionValues,
        "window-management": OptionValues,
        "xr-spatial-tracking": OptionValues
    },
    total=False
)

class PermissionsPolicy:
    '''PermissionsPolicy class sets Permissions-Policy header.

    Example :
        app.add_middleware(PermissionsPolicy, Option={})

    Parameters :
       Option (PermissionsPolicyOptions): The options for the permission policy.
    
    '''
    def __init__(self, app: ASGIApp, Option: PermissionsPolicyOptions = {}):
        """
        Initializes a new instance of the class.

        Parameters:
            app (ASGIApp): The application object.
            Option (PermissionsPolicyOptions): The options for the permission policy.

        Raises:
            SyntaxError: If the `Option` parameter is empty.

        Warning:
            The `Permission-Policy` header is still under working draft, browsers might give warnings and errors.

        Returns:
            None
        """
        self.app = app
        self.PolicyString = ''
        Policy: list[str] = ["accelerometer", "ambient-light-sensor", "aria-notify", "attribution-reporting", "autoplay", "bluetooth", "browsing-topics", "camera", "captured-surface-control", "compute-pressure", "cross-origin-isolated", "deferred-fetch", "deferred-fetch-minimal", "display-capture", "encrypted-media", "fullscreen", "geolocation", "gyroscope", "hid", "identity-credentials-get", "idle-detection", "local-fonts", "magnetometer", "microphone", "midi", "on-device-speech-recognition", "otp-credentials", "payment", "picture-in-picture", "private-state-token-issuance", "private-state-token-redemption", "publickey-credentials-create", "publickey-credentials-get", "screen-wake-lock", "serial", "storage-access", "summarizer", "usb", "web-share", "window-management", "xr-spatial-tracking"]
        if Option == {}:
            raise SyntaxError('Option cannot be empty for Permission-Policy to be applied')
        else:
            warn("Permission-Policy header is still under working draft, browsers might give warnings and errors", SyntaxWarning, 2)
            self.__PolicyCheck__(Option, Policy)
    
    def __PolicyCheck__(self, Option: PermissionsPolicyOptions, Policy: list[str]) -> None:
        """
        Generate a policy string based on the given Option and Policy dictionaries.

        Args:
            Option (PermissionsPolicyOptions): The Option dictionary.
            Policy (list[str]): The Policy dictionary.

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
            values: OptionValues = Option.get(key, OptionValues)

            if len(values) != 1:
                if "*" in values:
                    raise SyntaxError(f'Cannot use wildcard(*) with other allowlist.')
            else:
                if "*" in values:
                    self.PolicyString += "=*, "
                    continue

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
                if value != "self":
                    if value[0] != '"':
                        raise SyntaxError(f'Invalid allowlist item({ value }) for feature { key }. Allowlist item must be *, self or a quoted URL "https://example.com"')

                self.PolicyString += value

                if j == len(values) - 1:
                    if i == len(keys) - 1:
                        self.PolicyString += ')'
                    else:
                        self.PolicyString += '), '
                else:
                    self.PolicyString += ' '

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """
        Asynchronously handles HTTP requests by routing them to the appropriate handler based on the request path.

        Parameters:
            scope (Scope): The scope of the request.
            receive (Receive): A function that returns a coroutine that reads messages from the server.
            send (Send): A function that sends messages to the server.

        Returns:
            None
        """
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_Permissions_Policy(message: Message):
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
