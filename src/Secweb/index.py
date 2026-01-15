'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2026, Motagamwala Taha Arif Ali '''

from typing import Any, Literal, TypedDict, Union
from starlette.applications import Starlette

from .WsStrictTransportSecurity.WsStrictTransportSecurityMiddleware import WsHSTS, WsHSTSOptions
from .XFrameOptions.XFrameOptionsMiddleware import XFrame, XFrameOptions
from .CrossOriginEmbedderPolicy.CrossOriginEmbedderPolicyMiddleware import CrossOriginEmbedderPolicy, CrossOriginEmbedderPolicyOptions
from .CrossOriginOpenerPolicy.CrossOriginOpenerPolicyMiddleware import CrossOriginOpenerPolicy, CrossOriginOpenerPolicyOptions
from .CrossOriginResourcePolicy.CrossOriginResourcePolicyMiddleware import CrossOriginResourcePolicy, CrossOriginResourcePolicyOptions
from .xXSSProtection.xXSSProtectionMiddleware import xXSSProtection
from .StrictTransportSecurity.StrictTransportSecurityMiddleware import HSTS, HSTSOptions
from .XPermittedCrossDomainPolicies.XPermittedCrossDomainPoliciesMiddleware import XPermittedCrossDomainPolicies, XPermittedCrossDomainPoliciesOptions
from .XDownloadOptions.XDownloadOptionsMiddleware import XDownloadOptions
from .XDNSPrefetchControl.XDNSPrefetchControlMiddleware import XDNSPrefetchControl, XDNSPrefetchControlOptions
from .XContentTypeOptions.XContentTypeOptionsMiddleware import XContentTypeOptions
from .ReferrerPolicy.ReferrerPolicyMiddleware import ReferrerPolicy, ReferrerPolicyOptions
from .OriginAgentCluster.OriginAgentClusterMiddleware import OriginAgentCluster
from .ContentSecurityPolicy.ContentSecurityPolicyMiddleware import ContentSecurityPolicy, ContentSecurityPolicyOptions
from .PermissionsPolicy.PermissionsPolicyMiddleware import PermissionsPolicy, PermissionsPolicyOptions
from .ClearSiteData.ClearSiteDataMiddleware import ClearSiteData, ClearSiteDataOptions
from .CacheControl.CacheControlMiddleware import CacheControl, CacheControlOptions


SecWebOptions = TypedDict(
    'SecWebOptions',
    {
        'csp': Union[Literal[False], ContentSecurityPolicyOptions],
        'coop': Union[Literal[False], CrossOriginOpenerPolicyOptions],
        'coep': Union[Literal[False], CrossOriginEmbedderPolicyOptions],
        'corp': Union[Literal[False], CrossOriginResourcePolicyOptions],
        'referrer': Union[Literal[False], ReferrerPolicyOptions],
        'xdns': Union[Literal[False], XDNSPrefetchControlOptions],
        'xcdp': Union[Literal[False], XPermittedCrossDomainPoliciesOptions],
        'hsts': Union[Literal[False], HSTSOptions],
        'wshsts': Union[Literal[False], WsHSTSOptions],
        'xframe': Union[Literal[False], XFrameOptions],
        'PermissionPolicy': Union[Literal[False], PermissionsPolicyOptions],
        'clearSiteData': Union[Literal[False], ClearSiteDataOptions],
        'cacheControl': Union[Literal[False], CacheControlOptions],
        'xcto': Literal[False],
        'xdo': Literal[False],
        'xss': Literal[False],
        'oac': Literal[False]
    },
    total=False
)


class SecWeb:
    """This Class is used for initializing all the middlewares CSP, COOP, etc. you can also activate/deactivate any of the middlewares by supplying them boolean values in the Option parameter.

    Example :
        SecWeb(app=app, Option={'csp': {'default-src': ["'self'"]}, 'xframe': False}, Routes=[], report_only=False, script_nonce=False, style_nonce=False)

    Parameters :

     app=YourappName This is the compulsory parameter

     Option={} This is a dictionary and not compulsory parameter

     Routes=[] This is a list of routes for Clear-Site-Data header and a compulsory parameter if you want to use that header

     script_nonce=False This is an optional flag it will set nonce for your JS scripts

     style_nonce=False This is an optional flag it will set the nonce for your CSS stylesheets

     report_only=False This is an optional flag it will set the Content-Security-Policy-Report-Only header instead of the Content-Security-Policy header

    Values :
        'csp' for ContentSecurityPolicy

        'coop' for CrossOriginOpenerPolicy

        'coep' for CrossOriginEmbedderPolicy

        'corp' for CrossOriginResourcePolicy

        'referrer' for ReferrerPolicy

        'xdns' for XDNSPrefetchControl

        'xcdp' for XPermittedCrossDomainPolicies

        'hsts' for HSTS/StrictTransportSecurity

        'wshsts' for HSTS/StrictTransportSecurity for websockets

        'xframe' for XFrame

        'PermissionPolicy' for PermissionPoilcy

        'clearSiteData' for Clear-Site-Data

        'cacheControl' for Cache-Control

        'xcto' for X-Content-Type-Options

        'xdo' for X-Download-Options

        'xss' for x-xss-protection

        'oac' for Origin-Agent-Cluster

    This Values are for the Option parameter
    
    """

    def __init__(
        self,
        app: Starlette,
        Option: SecWebOptions = {},
        Routes: list[str] = [],
        script_nonce: bool = False,
        style_nonce: bool = False,
        report_only: bool = False
    ) -> None:

        """
        Initializes an instance of the class.

        Args:
            app: The application object.
            Option: A dictionary of options (default: {}).
            Routes: A list of routes for the Clear-Site-Data header (default: []).
            script_nonce: Whether to include script nonce (default: False).
            style_nonce: Whether to include style nonce (default: False).
            report_only: Whether to use Content-Security-Policy-Report-Only header instead of Content-Security-Policy (default: False).

        Returns:
            None
        """
        
        MIDDLEWARE_REGISTRY: dict[str, tuple[type, bool]] = {
            "xdo": (XDownloadOptions, True),
            "xcto": (XContentTypeOptions, True),
            "oac": (OriginAgentCluster, True),
            "xss": (xXSSProtection, True),
            "coop": (CrossOriginOpenerPolicy, True),
            "coep": (CrossOriginEmbedderPolicy, True),
            "corp": (CrossOriginResourcePolicy, True),
            "referrer": (ReferrerPolicy, True),
            "xdns": (XDNSPrefetchControl, True),
            "xcdp": (XPermittedCrossDomainPolicies, True),
            "hsts": (HSTS, True),
            "wshsts": (WsHSTS, True),
            "xframe": (XFrame, True),
            "cacheControl": (CacheControl, True),
            "PermissionPolicy": (PermissionsPolicy, False),
        }

        for key, (cls, default) in MIDDLEWARE_REGISTRY.items():
            val = Option.get(key)
            if val is False:
                continue
            
            if val is not None:
                app.add_middleware(cls, val)
            elif default:
                app.add_middleware(cls)

        csp_val = Option.get("csp")
        if csp_val is not False:
            csp_args: dict[str, Any] = {
                "script_nonce": script_nonce, 
                "style_nonce": style_nonce, 
                "report_only": report_only,
            }
            if isinstance(csp_val, dict):
                csp_args.update([("Option", csp_val)])
            app.add_middleware(ContentSecurityPolicy, **csp_args)

        csd_val = Option.get("clearSiteData")
        if csd_val is not False:
            if isinstance(csd_val, dict):
                app.add_middleware(ClearSiteData, csd_val, Routes=Routes)
            elif len(Routes) > 0:
                app.add_middleware(ClearSiteData, Routes=Routes)
