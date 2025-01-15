'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2025, Motagamwala Taha Arif Ali '''

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
from .ClearSiteData.ClearSiteDataMiddleware import ClearSiteData
from .CacheControl.CacheControlMiddleware import CacheControl

class SecWeb:
    """This Class is used for initializing all the middlewares CSP, COOP, etc.
       Now you can also activate/deactivate any of the middlewares by supplying them boolean values in the Option parameter.

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
        app,
        Option = {},
        Routes = [],
        script_nonce = False,
        style_nonce = False,
        report_only = False
    ) -> None:
        """
        Initializes an instance of the class.

        Args:
            app: The application object.
            Option: A dictionary of options (default: {}).
            Routes: A list of routes (default: []).
            script_nonce: Whether to include script nonce (default: False).
            style_nonce: Whether to include style nonce (default: False).
            report_only: Whether to use Content-Security-Policy-Report-Only header instead of Content-Security-Policy (default: False).

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
            app.add_middleware(ContentSecurityPolicy,script_nonce=script_nonce,style_nonce=style_nonce,report_only=report_only)
            app.add_middleware(CacheControl)
            app.add_middleware(CrossOriginEmbedderPolicy)
            app.add_middleware(CrossOriginOpenerPolicy)
            app.add_middleware(CrossOriginResourcePolicy)
            if Routes.__len__() > 0:
                app.add_middleware(ClearSiteData, Routes=Routes)
        else:
            if "xdo" in Option.keys() and Option["xdo"] is False:
                pass
            else:
                app.add_middleware(XDownloadOptions)
            if "xcto" in Option.keys() and Option['xcto'] is False:
                pass
            else:
                app.add_middleware(XContentTypeOptions)
            if "oac" in Option.keys() and Option['oac'] is False:
                pass
            else:
                app.add_middleware(OriginAgentCluster)
            if "xss" in Option.keys() and Option['xss'] is False:
                pass
            else:
                app.add_middleware(xXSSProtection)

            if "csp" in Option.keys() and Option["csp"] is not False:
                app.add_middleware(ContentSecurityPolicy,Option=Option["csp"],script_nonce=script_nonce,style_nonce=style_nonce,report_only=report_only)
            elif "csp" in Option.keys() and Option["csp"] is False:
                pass
            else:
                app.add_middleware(ContentSecurityPolicy,script_nonce=script_nonce,style_nonce=style_nonce,report_only=report_only)

            if "coop" in Option.keys() and Option["coop"] is not False:
                app.add_middleware(CrossOriginOpenerPolicy, Option=Option["coop"])
            elif "coop" in Option.keys() and Option["coop"] is False:
                pass
            else:
                app.add_middleware(CrossOriginOpenerPolicy)

            if "coep" in Option.keys() and Option["coep"] is not False:
                app.add_middleware(CrossOriginEmbedderPolicy, Option=Option["coep"])
            elif "coep" in Option.keys() and Option["coep"] is False:
                pass
            else:
                app.add_middleware(CrossOriginEmbedderPolicy)

            if "corp" in Option.keys() and Option["corp"] is not False:
                app.add_middleware(CrossOriginResourcePolicy, Option=Option["corp"])
            elif "corp" in Option.keys() and Option["corp"] is False:
                pass
            else:
                app.add_middleware(CrossOriginResourcePolicy)

            if "referrer" in Option.keys() and Option["referrer"] is not False:
                app.add_middleware(ReferrerPolicy, Option=Option["referrer"])
            elif "referrer" in Option.keys() and Option["referrer"] is False:
                pass
            else:
                app.add_middleware(ReferrerPolicy)

            if "xdns" in Option.keys() and Option["xdns"] is not False:
                app.add_middleware(XDNSPrefetchControl, Option=Option["xdns"])
            elif "xdns" in Option.keys() and Option["xdns"] is False:
                pass
            else:
                app.add_middleware(XDNSPrefetchControl)

            if "xcdp" in Option.keys() and Option["xcdp"] is not False:
                app.add_middleware(XPermittedCrossDomainPolicies, Option=Option["xcdp"])
            elif "xcdp" in Option.keys() and Option["xcdp"] is False:
                pass
            else:
                app.add_middleware(XPermittedCrossDomainPolicies)

            if "hsts" in Option.keys() and Option["hsts"] is not False:
                app.add_middleware(HSTS, Option=Option["hsts"])
            elif "hsts" in Option.keys() and Option["hsts"] is False:
                pass
            else:
                app.add_middleware(HSTS)
            
            if "wshsts" in Option.keys() and Option["wshsts"] is not False:
                app.add_middleware(WsHSTS, Option=Option["wshsts"])
            elif "wshsts" in Option.keys() and Option["wshsts"] is False:
                pass
            else:
                app.add_middleware(WsHSTS)

            if "xframe" in Option.keys() and Option["xframe"] is not False:
                app.add_middleware(XFrame, Option=Option["xframe"])
            elif "xframe" in Option.keys() and Option["xframe"] is False:
                pass
            else:
                app.add_middleware(XFrame)

            if "clearSiteData" in Option.keys() and Routes.__len__() > 0 and Option["clearSiteData"] is not False:
                app.add_middleware(ClearSiteData, Option=Option["clearSiteData"], Routes=Routes)
            else:
                pass

            if Routes.__len__() > 0:
                if "clearSiteData" in Option.keys() and Option["clearSiteData"] is False:
                    pass
                else:
                    app.add_middleware(ClearSiteData, Routes=Routes)

            if "cacheControl" in Option.keys() and Option["cacheControl"] is not False:
                app.add_middleware(CacheControl, Option=Option["cacheControl"])
            elif "cacheControl" in Option.keys() and Option["cacheControl"] is False:
                pass
            else:
                app.add_middleware(CacheControl)
