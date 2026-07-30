from __future__ import annotations
import typing
from typing import TYPE_CHECKING

from . import headers
from .middleware import SetMiddleware

if TYPE_CHECKING:
    from starlette.applications import Starlette
    from ._types import SecWeb_Options


class SecWeb:
    """
    A class that configures and applies security-related HTTP headers to a Starlette application.
    """
    def __init__(self, app: Starlette, options: SecWeb_Options = {}, script_nonce: bool = False, style_nonce: bool = False, csp_report_only: bool = False, coep_report_only: bool = False):
        """
        Initializes the SecWeb instance and injects the configured security headers into the application via middleware.

        It parses the provided `options` dictionary to selectively apply various HTTP security headers 
        like COEP, COOP, CSP, HSTS, etc. If a specific header configuration is explicitly set to False, 
        that header will not be applied.

        Args:
            app (Starlette): The Starlette application instance to which the middleware will be attached.
            options (SecWeb_Options, optional): A dictionary of header configurations. Supported keys include 
                'coep', 'coop', 'corp', 'xss', 'xcdp', 'xframe', 'xdns', 'xdo', 'xcto', 'oac', 'referrer', 
                'cache_control', 'hsts', 'wshsts', 'csp'. Defaults to {}.
            script_nonce (bool, optional): If True, generates and includes a nonce for inline scripts in the CSP. Defaults to False.
            style_nonce (bool, optional): If True, generates and includes a nonce for inline styles in the CSP. Defaults to False.
            csp_report_only (bool, optional): If True, configures CSP to operate in report-only mode. Defaults to False.
            coep_report_only (bool, optional): If True, configures COEP to operate in report-only mode. Defaults to False.

        Example:
            >>> app = FastAPI()
            >>> SecWeb(app, options={'hsts': {'max-age': 31536000}, 'xframe': 'DENY'})
        """
        Headers: list[tuple[bytes, bytes]] = []
        WS_HSTS: tuple[bytes, bytes] | None = None
        Dynamic_Headers: list = []
        val = options.get('coep')
        if val is not False:
            Headers.append(headers.Cross_Origin_Embedder_Policy(option=val, report_only=coep_report_only)) if val is not None else Headers.append(headers.Cross_Origin_Embedder_Policy(report_only=coep_report_only))
        val = options.get('coop')
        if val is not False:
            Headers.append(headers.Cross_Origin_Opener_Policy(option=val)) if val is not None else Headers.append(headers.Cross_Origin_Opener_Policy())
        val = options.get('corp')
        if val is not False:
            Headers.append(headers.Cross_Origin_Resource_Policy(option=val)) if val is not None else Headers.append(headers.Cross_Origin_Resource_Policy())
        val = options.get('xss')
        if val is not False:
            Headers.append(headers.X_XSS_Protection())
        val = options.get('xcdp')
        if val is not False:
            Headers.append(headers.X_Permitted_Cross_Domain_Policies(option=val)) if val is not None else Headers.append(headers.X_Permitted_Cross_Domain_Policies())
        val = options.get('xframe')
        if val is not False:
            Headers.append(headers.X_Frame(option=val)) if val is not None else Headers.append(headers.X_Frame())
        val = options.get('xdns')
        if val is not False:
            Headers.append(headers.X_DNS_Prefetch_Control(option=val)) if val is not None else Headers.append(headers.X_DNS_Prefetch_Control())
        val = options.get('xdo')
        if val is not False:
            Headers.append(headers.X_Download_Options())
        val = options.get('xcto')
        if val is not False:
            Headers.append(headers.X_Content_Type_Options())
        val = options.get('oac')
        if val is not False:
            Headers.append(headers.Origin_Agent_Cluster())
        val = options.get('referrer')
        if val is not False:
            Headers.append(headers.Referrer_Policy(option=val)) if val is not None else Headers.append(headers.Referrer_Policy())
        val = options.get('cache_control')
        if val is not False:
            Headers.append(headers.Cache_Control(options=val)) if val is not None else Headers.append(headers.Cache_Control())
        val = options.get('hsts')
        if val is not False:
            Headers.append(headers.HSTS(options=val)) if val is not None else Headers.append(headers.HSTS())
        val = options.get('wshsts')
        if val is not False:
            WS_HSTS = headers.WsHSTS(options=val) if val is not None else headers.WsHSTS()

        val = options.get('csp')
        if val is not False:
            csp_result = headers.Content_Security_Policy(options=val, script_nonce_flag=script_nonce, style_nonce_flag=style_nonce, report_only=csp_report_only) if val is not None else headers.Content_Security_Policy(script_nonce_flag=script_nonce, style_nonce_flag=style_nonce, report_only=csp_report_only)
            if callable(csp_result):
                Dynamic_Headers.append(csp_result)
            else:
                Headers.append(typing.cast('tuple[bytes, bytes]', csp_result))

        app.add_middleware(SetMiddleware, headers=Headers, wshsts=WS_HSTS, dynamic_headers=Dynamic_Headers)
