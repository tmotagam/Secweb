'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2024, Motagamwala Taha Arif Ali '''

from warnings import warn
from .WsStrictTransportSecurity.WsStrictTransportSecurityMiddleware import WsHSTS
from .XFrameOptions.XFrameOptionsMiddleware import XFrame
from .CrossOriginEmbedderPolicy.CrossOriginEmbedderPolicyMiddleware import CrossOriginEmbedderPolicy
from .CrossOriginOpenerPolicy.CrossOriginOpenerPolicyMiddleware import CrossOriginOpenerPolicy
from .CrossOriginResourcePolicy.CrossOriginResourcePolicyMiddleware import CrossOriginResourcePolicy
from .xXSSProtection.xXSSProtectionMiddleware import xXSSProtection
from .StrictTransportSecurity.StrictTransportSecurityMiddleware import HSTS
from .XPermittedCrossDomainPolicies.XPermittedCrossDomainPoliciesMiddleware import XPermittedCrossDomainPolicies
from .XDownloadOptions.XDownloadOptionsMiddleware import XDownloadOptions
from .XDNSPrefetchControl.XDNSPrefetchControlMiddleware import XDNSPrefetchControl
from .XContentTypeOptions.XContentTypeOptionsMiddleware import XContentTypeOptions
from .ReferrerPolicy.ReferrerPolicyMiddleware import ReferrerPolicy
from .OriginAgentCluster.OriginAgentClusterMiddleware import OriginAgentCluster
from .ContentSecurityPolicy.ContentSecurityPolicyMiddleware import ContentSecurityPolicy
from .PermissionsPolicy.PermissionsPolicyMiddleware import PermissionsPolicy
from .ClearSiteData.ClearSiteDataMiddleware import ClearSiteData
from .CacheControl.CacheControlMiddleware import CacheControl

class SecWeb:
    """This Class is used for initializing all the middlewares CSP, COOP, etc

    Example :
        SecWeb(app=app, Option={'csp': {'default-src': ["'self'"]}}, Routes=[], script_nonce=False, style_nonce=False)

    Parameters :

     app=YourappName This is the compulsory parameter

     Option={} This is a dictionary and not compulsory parameter

     Routes=[] This is a list of routes for Clear-Site-Data header and a compulsory parameter if you want to use that header

     script_nonce=False This is an optional flag it will set nonce for your JS scripts

     style_nonce=False This is an optional flag it will set the nonce for your CSS stylesheets

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

    This Values are for the Option parameter
    
    """

    def __init__(
        self,
        app,
        Option = {},
        Routes = [],
        script_nonce = False,
        style_nonce = False,
    ) -> None:
        """
        Initializes an instance of the class.

        Args:
            app: The application object.
            Option: A dictionary of options (default: {}).
            Routes: A list of routes (default: []).
            script_nonce: Whether to include script nonce (default: False).
            style_nonce: Whether to include style nonce (default: False).

        Returns:
            None
        """
        if not Option:
            app.add_middleware(XFrame)
            app.add_middleware(xXSSProtection)
            app.add_middleware(HSTS)
            app.add_middleware(WsHSTS)
            app.add_middleware(XPermittedCrossDomainPolicies)
            app.add_middleware(XDownloadOptions)
            app.add_middleware(XDNSPrefetchControl)
            app.add_middleware(XContentTypeOptions)
            app.add_middleware(ReferrerPolicy)
            app.add_middleware(OriginAgentCluster)
            app.add_middleware(ContentSecurityPolicy,script_nonce=script_nonce,style_nonce=style_nonce)
            app.add_middleware(CacheControl)
            app.add_middleware(CrossOriginEmbedderPolicy)
            app.add_middleware(CrossOriginOpenerPolicy)
            if Routes.__len__() > 0:
                app.add_middleware(ClearSiteData, Routes=Routes)
        else:
            app.add_middleware(XDownloadOptions)
            app.add_middleware(XContentTypeOptions)
            app.add_middleware(OriginAgentCluster)
            app.add_middleware(xXSSProtection)

            if "csp" in Option.keys():
                app.add_middleware(ContentSecurityPolicy,Option=Option["csp"],script_nonce=script_nonce,style_nonce=style_nonce)
            else:
                app.add_middleware(ContentSecurityPolicy,script_nonce=script_nonce,style_nonce=style_nonce)

            if "coop" in Option.keys():
                app.add_middleware(CrossOriginOpenerPolicy, Option=Option["coop"])
            else:
                app.add_middleware(CrossOriginOpenerPolicy)

            if "coep" in Option.keys():
                app.add_middleware(CrossOriginEmbedderPolicy, Option=Option["coep"])
            else:
                app.add_middleware(CrossOriginEmbedderPolicy)

            if "corp" in Option.keys():
                app.add_middleware(CrossOriginResourcePolicy, Option=Option["corp"])

            if "expectCt" in Option.keys():
                warn("Expect-CT Header is now deprecated by browsers and is removed from the library", SyntaxWarning, 2)

            if "referrer" in Option.keys():
                app.add_middleware(ReferrerPolicy, Option=Option["referrer"])
            else:
                app.add_middleware(ReferrerPolicy)

            if "xdns" in Option.keys():
                app.add_middleware(XDNSPrefetchControl, Option=Option["xdns"])
            else:
                app.add_middleware(XDNSPrefetchControl)

            if "xcdp" in Option.keys():
                app.add_middleware(XPermittedCrossDomainPolicies, Option=Option["xcdp"])
            else:
                app.add_middleware(XPermittedCrossDomainPolicies)

            if "hsts" in Option.keys():
                app.add_middleware(HSTS, Option=Option["hsts"])
            else:
                app.add_middleware(HSTS)
            
            if "wshsts" in Option.keys():
                app.add_middleware(WsHSTS, Option=Option["wshsts"])
            else:
                app.add_middleware(WsHSTS)

            if "xframe" in Option.keys():
                app.add_middleware(XFrame, Option=Option["xframe"])
            else:
                app.add_middleware(XFrame)

            if "PermissionPolicy" in Option.keys():
                app.add_middleware(PermissionsPolicy, Option=Option["PermissionPolicy"])

            if "clearSiteData" in Option.keys() and Routes.__len__() > 0:
                app.add_middleware(ClearSiteData, Option=Option["clearSiteData"], Routes=Routes)

            if Routes.__len__() > 0:
                app.add_middleware(ClearSiteData, Routes=Routes)

            if "cacheControl" in Option.keys():
                app.add_middleware(CacheControl, Option=Option["cacheControl"])
            else:
                app.add_middleware(CacheControl)
