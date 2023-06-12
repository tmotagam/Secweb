'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2023, Motagamwala Taha Arif Ali '''

from warnings import warn
from starlette.types import Scope, Receive, Send, ASGIApp, Message
from starlette.datastructures import MutableHeaders

class PermissionsPolicy:
    '''PermissionsPolicy class takes one prarameter Option for
    creating your Permissions-Policy header

    Example :
        app.add_middleware(PermissionsPolicy, Option={})

    Parameters :

    Option={} This is a dictionary'''
    def __init__(self, app: ASGIApp, Option: dict[str, list[str]] = {}):
        self.app = app
        self.PolicyString = ''
        Policy = ["accelerometer", "ambient-light-sensor", "autoplay", "battery", "camera", "display-capture", "document-domain", "encrypted-media", "execution-while-not-rendered", "execution-while-out-of-viewport", "fullscreen", "gamepad", "geolocation", "gyroscope", "hid", "identity-credentials-get", "idle-detection", "local-fonts", "magnetometer", "microphone", "midi", "payment", "picture-in-picture", "publickey-credentials-create", "publickey-credentials-get", "screen-wake-lock", "serial", "speaker-selection", "storage-access", "usb", "web-share", "xr-spatial-tracking"]
        if Option == {}:
            raise SyntaxError('Option cannot be empty for Permission-Policy to be applied')
        else:
            warn("Permission-Policy header is still under working draft, browsers might give warnings and errors", SyntaxWarning, 2)
            self.__PolicyCheck__(Option, Policy)
    
    def __PolicyCheck__(self, Option: dict[str, list[str]], Policy: list[str]):
        keys = list(Option.keys())

        for i in range(len(keys)):
            if keys[i] in Policy:
                self.PolicyString += keys[i]
                values = Option[keys[i]]
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

                for j in range(len(values)):
                    if values[j] != 'self' and values[j] != '*':
                        vch = values[j]
                        if vch[0] != '"':
                            raise SyntaxError(
                                f'Invalid allowlist item({ vch }) for feature { keys[i] }. Allowlist item must be *, self or quoted url "https://example.com" ')

                    self.PolicyString += values[j]
                    if j == len(values) - 1:
                        if i == len(keys) - 1:
                            self.PolicyString += ')'
                        else:
                            self.PolicyString += '), '
                    else:
                        self.PolicyString += ' '
            else:
                raise SyntaxError(f'The Policy { keys[i] } does not exists')

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_Permissions_Policy(message: Message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append('Permissions-Policy', self.PolicyString)

            await send(message)

        await self.app(scope, receive, set_Permissions_Policy)
