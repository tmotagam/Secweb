'''  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at https://mozilla.org/MPL/2.0/.

  Copyright 2021-2022, Motagamwala Taha Arif Ali '''

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class XPermittedCrossDomainPolicies(BaseHTTPMiddleware):
    ''' XPermittedCrossDomainPolicies class sets X-Permitted-Cross-Domain-Policies header it takes one Parameter

    Example:
        app.add_middleware(XPermittedCrossDomainPolicies, Option={})

    Parameter:

    Option={} This is a dictionary'''

    def __init__(self, app: ASGIApp, Option: dict = {'X-Permitted-Cross-Domain-Policies': 'none'}) -> None:
        super().__init__(app)
        self.Option = Option
        self.Policies = ['none', 'master-only', 'by-content-type', 'all']

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if self.Option['X-Permitted-Cross-Domain-Policies'] in self.Policies:
            response.headers['X-Permitted-Cross-Domain-Policies'] = self.Option['X-Permitted-Cross-Domain-Policies']
        else:
            raise SyntaxError(
                'X-Permitted-Cross-Domain-Policies has four values 1> "none" 2> "master-only" 3> "by-content-type" 4> "all"')
        return response
