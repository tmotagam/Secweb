'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021, Motagamwala Taha Arif Ali '''

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
import secrets

nonce = None


def Nonce_Processor(DEFAULT_ENTROPY=90):
    ''' This is the Nonce Processor module that will create the nonce for inline style and script
    It will be needed to call on the route which needs nonce for the inline script and css

    Example :
        @app.get("/")
        async def root():
            nonce = Nonce_Processor(DEFAULT_ENTROPY=20)  # inject the nonce variable into the jinja or html

    Parameter :
    DEFAULT_ENTROPY=20 This option sets the default entropy of the secrets module used for generating nonce'''
    global nonce
    secrets.DEFAULT_ENTROPY = DEFAULT_ENTROPY
    nonce = secrets.token_urlsafe()
    return nonce


class ContentSecurityPolicy(BaseHTTPMiddleware):
    ''' ContentSecurityPolicy class takes three prarameters script_nonce, style_nonce, Option for
    creating your csp header

    Example :
        app.add_middleware(ContentSecurityPolicy, Option={}, script_nonce=False, style_nonce=True)

    Parameters :

    Option={} This is a dictionary

    script_nonce=False This is the nonce flag for script

    style_nocne=True This is the nonce flag for style css'''
    def __init__(self, app: ASGIApp, script_nonce: bool = False, style_nonce: bool = False, Option: dict = {'default-src': ["'self'"], 'base-uri': ["'self'"], 'block-all-mixed-content': [], 'font-src': ["'self'", 'https:', 'data:'], 'frame-ancestors': ["'self'"], 'img-src': ["'self'", 'data:'], "object-src": ["'none'"], "script-src": ["'self'"], "script-src-attr": ["'none'"], "style-src": ["'self'", "https:", "'unsafe-inline'"], "upgrade-insecure-requests": [], "require-trusted-types-for": ["'script'"]}) -> None:
        super().__init__(app)
        self.Option = Option
        self.script_nonce = script_nonce
        self.style_nonce = style_nonce
        self.PolicyString = ''
        self.Policy = ['child-src', 'connect-src', 'default-src', 'font-src', 'frame-src', 'img-src', 'manifest-src', 'media-src', 'object-src', 'prefetch-src', 'script-src', 'script-src-elem', 'script-src-attr', 'style-src', 'style-src-elem', 'style-src-attr', 'worker-src', 'base-uri', 'plugin-types', 'sandbox', 'form-action', 'frame-ancestors', 'navigate-to', 'report-uri', 'report-to', 'block-all-mixed-content', 'require-sri-for', 'require-trusted-types-for', 'trusted-types', 'upgrade-insecure-requests', 'nonce']

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        self.__PolicyCheck__()
        response.headers['Content-Security-Policy'] = self.PolicyString
        return response

    def __PolicyCheck__(self):
        self.PolicyString = ''
        keys = list(self.Option.keys())

        if self.script_nonce is True:
            if not keys.index('script-src'):
                raise SyntaxError('script-src is compulsory for nonce')

            if len(self.Option['script-src']) == 0:
                raise SyntaxError('script-src cannot be empty for nonce to be applied')

        if self.style_nonce is True:
            if not keys.index('style-src'):
                raise SyntaxError('style-src is compulsory for nonce')

            if len(self.Option['style-src']) == 0:
                raise SyntaxError('style-src cannot be empty for nonce to be applied')

        for i in range(len(keys)):
            if keys[i] in self.Policy:
                self.PolicyString += keys[i]
                values = self.Option[keys[i]]
                if i == len(keys) - 1:
                    if len(values) != 0:
                        self.PolicyString += " "
                    else:
                        self.PolicyString += ''
                elif len(values) == 0:
                    self.PolicyString += '; '
                else:
                    self.PolicyString += " "

                if keys[i] == 'script-src' and self.script_nonce is True:
                    self.PolicyString += "'nonce-" + nonce + "' "

                if keys[i] == 'style-src' and self.style_nonce is True:
                    self.PolicyString += "'nonce-" + nonce + "' "

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
                raise SyntaxError(f'The Policy { keys[i] } does not exist')
