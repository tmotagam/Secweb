'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2026, Motagamwala Taha Arif Ali '''

from secrets import token_urlsafe
from typing import TypedDict
from warnings import warn
from starlette.types import Send, Receive, Scope, Message, ASGIApp

from starlette.datastructures import MutableHeaders

style_nonce = None
script_nonce = None

ContentSecurityPolicyOptions = TypedDict(
    'ContentSecurityPolicyOptions',
    {
        'child-src': list[str],
        'connect-src': list[str],
        'default-src': list[str],
        'font-src': list[str],
        'frame-src': list[str],
        'img-src': list[str],
        'manifest-src': list[str],
        'media-src': list[str],
        'object-src': list[str],
        'script-src': list[str],
        'script-src-elem': list[str],
        'script-src-attr': list[str],
        'style-src': list[str],
        'style-src-elem': list[str],
        'style-src-attr': list[str],
        'worker-src': list[str],
        'base-uri': list[str],
        'plugin-types': list[str],
        'sandbox': list[str],
        'form-action': list[str],
        'frame-ancestors': list[str],
        'navigate-to': list[str],
        'report-uri': list[str],
        'report-to': list[str],
        'block-all-mixed-content': list[str],
        'require-trusted-types-for': list[str],
        'trusted-types': list[str],
        'upgrade-insecure-requests': list[str],
        'fenced-frame-src': list[str]
    }, total=False
)

def Nonce_Processor(DEFAULT_ENTROPY: int = 90) -> str:
    """
    Generate a nonce using the `token_urlsafe` function.

    Args:
        DEFAULT_ENTROPY (int, optional): The entropy value for generating the nonce. (default: 90).

    Returns:
        str: The generated nonce.

    """
    global style_nonce
    global script_nonce
    style_nonce = token_urlsafe(DEFAULT_ENTROPY)
    script_nonce = style_nonce
    return style_nonce

class ContentSecurityPolicy:
    ''' ContentSecurityPolicy class sets Content-Security-Policy/Content-Security-Policy-Report-Only header.

    Example :
        app.add_middleware(ContentSecurityPolicy, Option={}, script_nonce=False, report_only=False, style_nonce=True)

    Parameters :
        script_nonce (bool, optional): The script_nonce parameter. Defaults to False.
        style_nonce (bool, optional): The style_nonce parameter. Defaults to False.
        report_only (bool, optional): The report_only parameter. Defaults to False.
        Option (ContentSecurityPolicyOptions, optional): The Option parameter. Defaults to {'default-src': ["'self'"], 'base-uri': ["'self'"], 'block-all-mixed-content': [], 'font-src': ["'self'", 'https:', 'data:'], 'frame-ancestors': ["'self'"], 'img-src': ["'self'", 'data:'], "object-src": ["'none'"], "script-src": ["'self'"], "script-src-attr": ["'none'"], "style-src": ["'self'", "https:", "'unsafe-inline'"], "upgrade-insecure-requests": [], "require-trusted-types-for": ["'script'"]}.
    
    '''
    def __init__(self, app: ASGIApp, script_nonce: bool = False, report_only: bool = False, style_nonce: bool = False, Option: ContentSecurityPolicyOptions = {'default-src': ["'self'"], 'base-uri': ["'self'"], 'block-all-mixed-content': [], 'font-src': ["'self'", 'https:', 'data:'], 'frame-ancestors': ["'self'"], 'img-src': ["'self'", 'data:'], "object-src": ["'none'"], "script-src": ["'self'"], "script-src-attr": ["'none'"], "style-src": ["'self'", "https:", "'unsafe-inline'"], "upgrade-insecure-requests": [], "require-trusted-types-for": ["'script'"]}):
        """
        Initialize the class with the given parameters.

        Parameters:
            app (ASGIApp): The app parameter.
            script_nonce (bool, optional): The script_nonce parameter. Defaults to False.
            style_nonce (bool, optional): The style_nonce parameter. Defaults to False.
            Option (ContentSecurityPolicyOptions, optional): The Option parameter. Defaults to {'default-src': ["'self'"], 'base-uri': ["'self'"], 'block-all-mixed-content': [], 'font-src': ["'self'", 'https:', 'data:'], 'frame-ancestors': ["'self'"], 'img-src': ["'self'", 'data:'], "object-src": ["'none'"], "script-src": ["'self'"], "script-src-attr": ["'none'"], "style-src": ["'self'", "https:", "'unsafe-inline'"], "upgrade-insecure-requests": [], "require-trusted-types-for": ["'script'"]}.

        Returns:
            None
        """
        self.app = app
        self.PolicyString = ''
        self.ReportOnly = report_only
        self.HeaderName = 'Content-Security-Policy' if not report_only else 'Content-Security-Policy-Report-Only'
        self.script_nonce = script_nonce
        self.style_nonce = style_nonce
        Policy: list[str] = ['child-src', 'connect-src', 'default-src', 'font-src', 'frame-src', 'img-src', 'manifest-src', 'media-src', 'object-src', 'script-src', 'script-src-elem', 'script-src-attr', 'style-src', 'style-src-elem', 'style-src-attr', 'worker-src', 'base-uri', 'plugin-types', 'sandbox', 'form-action', 'frame-ancestors', 'navigate-to', 'report-uri', 'report-to', 'block-all-mixed-content', 'require-trusted-types-for', 'trusted-types', 'upgrade-insecure-requests', 'fenced-frame-src']
        self.__PolicyCheck__(Option, Policy)
    
    def __PolicyCheck__(self, Option: ContentSecurityPolicyOptions, Policy: list[str]) -> None:
        """
        Check the policy for a given option and update the policy string.

        Parameters:
            Option (ContentSecurityPolicyOptions): A dictionary containing the policy options.
            Policy (list): A list of valid policy options.

        Raises:
            SyntaxError: If a required policy option is missing or if a policy option does not exist.

        Returns:
            None
        """
        keys = list(Option.keys())

        if self.ReportOnly is True and 'report-to' not in keys:
            if self.ReportOnly is True and 'report-uri' not in keys:
                raise SyntaxError('report-to and/or report-uri are compulsory for Content-Security-Policy-report-only')
        
        
        if self.ReportOnly is True and 'sandbox' in keys:
            warn('sandbox option is not supported in report-only policy', SyntaxWarning, 2)

        if self.script_nonce and 'script-src' not in keys:
            raise SyntaxError('script-src is compulsory for nonce')

        if self.style_nonce and 'style-src' not in keys:
            raise SyntaxError('style-src is compulsory for nonce')

        for i, key in enumerate(keys):
            if key not in Policy:
                raise SyntaxError(f'The Policy {key} does not exist')

            self.PolicyString += key
            values: list[str] = Option.get(key, [])

            if (key == 'script-src' and self.script_nonce and len(values) == 0) or (key == 'style-src' and self.style_nonce and len(values) == 0):
                self.PolicyString += " "
            elif i == len(keys) - 1:
                self.PolicyString += " " if len(values) != 0 else ''
            elif len(values) == 0:
                self.PolicyString += '; '
            else:
                self.PolicyString += " "

            if key == 'script-src' and self.script_nonce:
                self.PolicyString += "'nonce-{script_nonce_value}'" if i == len(keys) - 1 and len(values) == 0 else "'nonce-{script_nonce_value}'; " if len(values) == 0 else "'nonce-{script_nonce_value}' "

            if key == 'style-src' and self.style_nonce:
                self.PolicyString += "'nonce-{style_nonce_value}'" if i == len(keys) - 1 and len(values) == 0 else "'nonce-{style_nonce_value}'; " if len(values) == 0 else "'nonce-{style_nonce_value}' "

            for j, value in enumerate(values):
                self.PolicyString += value
                if j == len(values) - 1:
                    self.PolicyString += '' if i == len(keys) - 1 else '; '
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

        PS = self.PolicyString

        async def set_Content_Security_Policy(message: Message):
            """
            Sets the Content-Security-Policy header in the HTTP response.

            Args:
                message (Message): The message containing the type of the response.

            Returns:
                None

            """
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                if self.script_nonce is True and self.style_nonce is True:
                    headers.append(self.HeaderName, PS.format(script_nonce_value=script_nonce, style_nonce_value=style_nonce))
                elif self.style_nonce is True:
                    headers.append(self.HeaderName, PS.format(style_nonce_value=style_nonce))
                elif self.script_nonce is True:
                    headers.append(self.HeaderName, PS.format(script_nonce_value=script_nonce))
                else:
                    headers.append(self.HeaderName, PS)

            await send(message)

        await self.app(scope, receive, set_Content_Security_Policy)