'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2022, Motagamwala Taha Arif Ali '''

from starlette.types import ASGIApp

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
from .ExpectCt.ExpectCtMiddleware import ExpectCt
from .ContentSecurityPolicy.ContentSecurityPolicyMiddleware import ContentSecurityPolicy
from .PermissionsPolicy.PermissionsPolicyMiddleware import PermissionsPolicy
from .ClearSiteData.ClearSiteDataMiddleware import ClearSiteData
from .CacheControl.CacheControlMiddleware import CacheControl


class SecWeb():
    ''' This Class is used for initializing all the middlewares CSP, ExceptCt, etc

    Example :
        SecWeb(app=app, Option={'csp': {'default-src': ["'self'"]}}, Routes=[], script_nonce=False, style_nonce=False)

    Parameters :

     app=YourappName This is the compulsory parameter

     Option={} This is a dictionary and not compulsory option

     Routes=[] This is a list of routes for Clear-Site-Data header and a compulsory option if you want to use the header

     script_nonce=False This is an optional flag it will set nonce for your inline Js script

     style_nonce=False This is an optional flag it will set the nonce for your inline css

    Values :
        'csp' for ContentSecurityPolicy

        'coop' for CrossOriginOpenerPolicy

        'coep' for CrossOriginEmbedderPolicy

        'corp' for CrossOriginResourcePolicy

        'expectCt' for ExpectCt

        'referrer' for ReferrerPolicy

        'xdns' for XDNSPrefetchControl

        'xcdp' for XPermittedCrossDomainPolicies

        'hsts' for HSTS/StrictTransportSecurity

        'xss' for xXSSProtection

        'xframe' for XFrame

        'PermissionPolicy' for PermissionPoilcy

        'clearSiteData' for Clear-Site-Data

        'cacheControl' for Cache-Control

    This Values are for Option parameter'''

    def __init__(self, app: ASGIApp, Option: dict = {}, Routes: list = [], script_nonce: bool = False, style_nonce: bool = False) -> None:
        if not Option:
            app.add_middleware(XFrame)
            app.add_middleware(xXSSProtection)
            app.add_middleware(HSTS)
            app.add_middleware(XPermittedCrossDomainPolicies)
            app.add_middleware(XDownloadOptions)
            app.add_middleware(XDNSPrefetchControl)
            app.add_middleware(XContentTypeOptions)
            app.add_middleware(ReferrerPolicy)
            app.add_middleware(OriginAgentCluster)
            app.add_middleware(
                ContentSecurityPolicy, script_nonce=script_nonce, style_nonce=style_nonce)
            app.add_middleware(CacheControl)
            app.add_middleware(CrossOriginEmbedderPolicy)
            app.add_middleware(CrossOriginOpenerPolicy)
            if Routes.__len__() > 0:
                app.add_middleware(ClearSiteData, Routes=Routes)
        else:
            app.add_middleware(XDownloadOptions)
            app.add_middleware(XContentTypeOptions)
            app.add_middleware(OriginAgentCluster)

            if 'csp' in Option.keys():
                app.add_middleware(
                    ContentSecurityPolicy, Option=Option['csp'], script_nonce=script_nonce, style_nonce=style_nonce)
            else:
                app.add_middleware(
                    ContentSecurityPolicy, script_nonce=script_nonce, style_nonce=style_nonce)

            if 'coop' in Option.keys():
                app.add_middleware(CrossOriginOpenerPolicy,
                                   Option=Option['coop'])
            else:
                app.add_middleware(CrossOriginOpenerPolicy)

            if 'coep' in Option.keys():
                app.add_middleware(CrossOriginEmbedderPolicy,
                                   Option=Option['coep'])
            else:
                app.add_middleware(CrossOriginEmbedderPolicy)

            if 'corp' in Option.keys():
                app.add_middleware(CrossOriginResourcePolicy,
                                   Option=Option['corp'])

            if 'expectCt' in Option.keys():
                app.add_middleware(ExpectCt, Option=Option['expectCt'])

            if 'referrer' in Option.keys():
                app.add_middleware(ReferrerPolicy, Option=Option['referrer'])
            else:
                app.add_middleware(ReferrerPolicy)

            if 'xdns' in Option.keys():
                app.add_middleware(XDNSPrefetchControl, Option=Option['xdns'])
            else:
                app.add_middleware(XDNSPrefetchControl)

            if 'xcdp' in Option.keys():
                app.add_middleware(
                    XPermittedCrossDomainPolicies, Option=Option['xcdp'])
            else:
                app.add_middleware(XPermittedCrossDomainPolicies)

            if 'hsts' in Option.keys():
                app.add_middleware(HSTS, Option=Option['hsts'])
            else:
                app.add_middleware(HSTS)

            if 'xss' in Option.keys():
                app.add_middleware(xXSSProtection, Option=Option['xss'])
            else:
                app.add_middleware(xXSSProtection)

            if 'xframe' in Option.keys():
                app.add_middleware(XFrame, Option=Option['xframe'])
            else:
                app.add_middleware(XFrame)

            if 'PermissionPolicy' in Option.keys():
                app.add_middleware(PermissionsPolicy,
                                   Option=Option['PermissionPolicy'])

            if 'clearSiteData' in Option.keys() and Routes.__len__() > 0:
                app.add_middleware(
                    ClearSiteData, Option=Option['clearSiteData'], Routes=Routes)

            if Routes.__len__() > 0:
                app.add_middleware(ClearSiteData, Routes=Routes)

            if 'cacheControl' in Option.keys():
                app.add_middleware(CacheControl, Option=Option['cacheControl'])
            else:
                app.add_middleware(CacheControl)
