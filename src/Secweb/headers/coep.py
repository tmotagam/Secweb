from __future__ import annotations
from typing import TYPE_CHECKING

from ..middleware import SetMiddleware

if TYPE_CHECKING:
    from .._types import Cross_Origin_Embedder_Policy_Options
    from starlette.applications import Starlette

def Cross_Origin_Embedder_Policy(app: Starlette | None = None, option: Cross_Origin_Embedder_Policy_Options = {'unsafe-none': True}, report_only: bool = False) -> tuple[bytes, bytes]:
    """
    Sets the `Cross-Origin-Embedder-Policy` (COEP) HTTP response header.

    The COEP header prevents a document from loading any cross-origin resources that don't explicitly grant the document permission 
    (using CORP or CORS).

    Args:
        app (Starlette | None, optional): An optional Starlette application instance. 
            If provided, the COEP header is injected into the application via middleware. Defaults to None.
        option (Cross_Origin_Embedder_Policy_Options, optional): A dictionary specifying the policy.
            Valid main policies are 'require-corp', 'unsafe-none', and 'credentialless'. Exactly one main policy must be set to True.
            An optional 'report-to' endpoint can also be specified. Defaults to {'unsafe-none': True}.
        report_only (bool, optional): If True, sets the `Cross-Origin-Embedder-Policy-Report-Only` header instead, 
            which allows violations to be reported to the `report-to` endpoint without blocking resources. Defaults to False.

    Returns:
        tuple[bytes, bytes]: A tuple representing the header key and its computed value, 
            e.g., `(b"Cross-Origin-Embedder-Policy", b"require-corp")`.

    Raises:
        ValueError: If an unsupported option is provided.
        ValueError: If exactly one main policy is not provided.
        ValueError: If the value of the main policy is not True.
    
    Example:
        >>> Cross_Origin_Embedder_Policy(app, option={'require-corp': True, 'report-to': 'endpoint-name'})
        (b'Cross-Origin-Embedder-Policy', b'require-corp; report-to="endpoint-name"')
    """
    valid_main_policies = {'require-corp', 'unsafe-none', 'credentialless'}
    provided_keys = set(option)
    
    if provided_keys.difference(valid_main_policies.union({'report-to'})):
        raise ValueError('Invalid option for Cross-Origin-Embedder-Policy (Must be one of: require-corp, unsafe-none, credentialless, and optionally report-to)')
    
    main_policies_provided = provided_keys.intersection(valid_main_policies)
    if len(main_policies_provided) != 1:
        raise ValueError('You must provide exactly one main policy (require-corp, unsafe-none, or credentialless)')
        
    main_policy = list(main_policies_provided)[0]
    if option.get(main_policy) is not True:
        raise ValueError(f'The value for {main_policy} must be True')

    parts = [main_policy]
    if 'report-to' in option:
        parts.append(f'report-to="{option.get("report-to")}"')
        
    policy_value = '; '.join(parts).encode('latin-1')
    header_name = b'Cross-Origin-Embedder-Policy-Report-Only' if report_only else b'Cross-Origin-Embedder-Policy'
    
    if app is not None:
        app.add_middleware(SetMiddleware, headers=[(header_name, policy_value)])
    return (header_name, policy_value)
