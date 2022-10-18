'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2022, Motagamwala Taha Arif Ali '''

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

import warnings


class PermissionsPolicy(BaseHTTPMiddleware):
    '''PermissionsPolicy class takes one prarameter Option for
    creating your Permissions-Policy header

    Example :
        app.add_middleware(PermissionsPolicy, Option={})

    Parameters :

    Option={} This is a dictionary'''

    def __init__(self, app: ASGIApp, Option: dict = {}) -> None:
        super().__init__(app)
        self.Option = Option
        self.PolicyString = ''
        self.Policy = ["accelerometer",
                       "ambient-light-sensor",
                       "autoplay",
                       "battery",
                       "camera",
                       "cross-origin-isolated",
                       "display-capture",
                       "document-domain",
                       "encrypted-media",
                       "execution-while-not-rendered",
                       "execution-while-out-of-viewport",
                       "fullscreen",
                       "geolocation",
                       "gyroscope",
                       "hid",
                       "idle-detection",
                       "magnetometer",
                       "microphone",
                       "midi",
                       "navigation-override",
                       "payment",
                       "picture-in-picture",
                       "publickey-credentials-get",
                       "screen-wake-lock",
                       "serial",
                       "sync-xhr",
                       "usb",
                       "web-share",
                       "xr-spatial-tracking",
                       "Client Hints",
                       "clipboard-read",
                       "clipboard-write",
                       "gamepad",
                       "speaker-selection",
                       "browsing-topics",
                       "conversion-measurement",
                       "focus-without-user-activation",
                       "sync-script",
                       "trust-token-redemption",
                       "unload",
                       "vertical-scroll",
                       "window-placement"]

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if self.Option == {}:
            raise SyntaxError(
                'Option cannot be empty for Permission-Policy to be applied')
        else:
            warnings.warn(
                "Permission-Policy header is still under working draft, browsers might give warnings and errors", SyntaxWarning, 2)
            self.__PolicyCheck__()

        response.headers['Permissions-Policy'] = self.PolicyString
        return response

    def __PolicyCheck__(self):
        self.PolicyString = ''
        keys = list(self.Option.keys())

        for i in range(len(keys)):
            if keys[i] in self.Policy:
                self.PolicyString += keys[i]
                values = self.Option[keys[i]]
                if i == len(keys) - 1:
                    if len(values) != 0:
                        self.PolicyString += " "
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
                            self.PolicyString += ''
                        else:
                            self.PolicyString += '), '
                    else:
                        self.PolicyString += ' '
            else:
                raise SyntaxError(f'The Policy { keys[i] } does not exists')
