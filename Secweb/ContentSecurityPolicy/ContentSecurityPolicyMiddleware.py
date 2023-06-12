'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2023, Motagamwala Taha Arif Ali '''

from secrets import token_urlsafe
from starlette.types import Scope, Receive, Send, ASGIApp, Message
from starlette.datastructures import MutableHeaders

nonce = None

def Nonce_Processor(DEFAULT_ENTROPY=90):
    ''' This is the Nonce Processor module that will create the nonce for inline style and script
    It will be needed to call on the route which needs nonce for the inline script and css

    Example :
        @app.get("/")
        async def root():
            nonce = Nonce_Processor(DEFAULT_ENTROPY=20)  # inject the nonce variable into the jinja or html

    Parameter :
    DEFAULT_ENTROPY=20 This option sets the default entropy used for generating nonce'''
    global nonce
    nonce = token_urlsafe(DEFAULT_ENTROPY)
    return nonce

class ContentSecurityPolicy:
    ''' ContentSecurityPolicy class takes three prarameters script_nonce, style_nonce, Option for
    creating your csp header

    Example :
        app.add_middleware(ContentSecurityPolicy, Option={}, script_nonce=False, style_nonce=True)

    Parameters :

    Option={} This is a dictionary

    script_nonce=False This is the nonce flag for script

    style_nocne=True This is the nonce flag for style css'''
    def __init__(self, app: ASGIApp, script_nonce: bool = False, style_nonce: bool = False, Option: dict[str, list[str]] = {'default-src': ["'self'"], 'base-uri': ["'self'"], 'block-all-mixed-content': [], 'font-src': ["'self'", 'https:', 'data:'], 'frame-ancestors': ["'self'"], 'img-src': ["'self'", 'data:'], "object-src": ["'none'"], "script-src": ["'self'"], "script-src-attr": ["'none'"], "style-src": ["'self'", "https:", "'unsafe-inline'"], "upgrade-insecure-requests": [], "require-trusted-types-for": ["'script'"]}):
        self.app = app
        self.PolicyString = ''
        self.script_nonce = script_nonce
        self.style_nonce = style_nonce
        Policy = ['child-src', 'connect-src', 'default-src', 'font-src', 'frame-src', 'img-src', 'manifest-src', 'media-src', 'object-src', 'script-src', 'script-src-elem', 'script-src-attr', 'style-src', 'style-src-elem', 'style-src-attr', 'worker-src', 'base-uri', 'plugin-types', 'sandbox', 'form-action', 'frame-ancestors', 'navigate-to', 'report-uri', 'report-to', 'block-all-mixed-content', 'require-trusted-types-for', 'trusted-types', 'upgrade-insecure-requests']
        self.__PolicyCheck__(Option, Policy)

    def __PolicyCheck__(self, Option: dict[str, list[str]], Policy: list[str]):
        keys = list(Option.keys())

        if self.script_nonce is True:
            if keys.index('script-src') is None:
                raise SyntaxError('script-src is compulsory for nonce')

        if self.style_nonce is True:
            if keys.index('style-src') is None:
                raise SyntaxError('style-src is compulsory for nonce')

        for i in range(len(keys)):
            if keys[i] in Policy:
                self.PolicyString += keys[i]
                values = Option[keys[i]]
                if (keys[i] == 'script-src' and self.script_nonce is True and len(values) == 0) or (keys[i] == 'style-src' and self.style_nonce is True and len(values) == 0):
                    self.PolicyString += " "
                elif i == len(keys) - 1:
                    if len(values) != 0:
                        self.PolicyString += " "
                    else:
                        self.PolicyString += ''
                elif len(values) == 0:
                    self.PolicyString += '; '
                else:
                    self.PolicyString += " "

                if keys[i] == 'script-src' and self.script_nonce is True:
                    self.PolicyString += "'nonce-{script_nonce_value}'" if i == len(keys) - 1 and len(values) == 0 else "'nonce-{script_nonce_value}'; " if len(values) == 0 else "'nonce-{script_nonce_value}' "

                if keys[i] == 'style-src' and self.style_nonce is True:
                    self.PolicyString += "'nonce-{style_nonce_value}'" if i == len(keys) - 1 and len(values) == 0 else "'nonce-{style_nonce_value}'; " if len(values) == 0 else "'nonce-{style_nonce_value}' "

                for j in range(len(values)):
                    self.PolicyString += values[j]
                    if j == len(values) - 1:
                        if i == len(keys) - 1:
                            self.PolicyString += ''
                        else:
                            self.PolicyString += '; '
                    else:
                        self.PolicyString += ' '
            else:
                raise SyntaxError(f'The Policy { keys[i] } does not exists')

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def set_Content_Security_Policy(message: Message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                if self.script_nonce is True and self.style_nonce is True:
                    PS = self.PolicyString
                    headers.append('Content-Security-Policy', PS.format(script_nonce_value=nonce, style_nonce_value=nonce))
                elif self.style_nonce is True:
                    PS = self.PolicyString
                    headers.append('Content-Security-Policy', PS.format(style_nonce_value=nonce))
                elif self.script_nonce is True:
                    PS = self.PolicyString
                    headers.append('Content-Security-Policy', PS.format(script_nonce_value=nonce))
                else:
                    headers.append('Content-Security-Policy', self.PolicyString)

            await send(message)

        await self.app(scope, receive, set_Content_Security_Policy)