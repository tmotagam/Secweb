from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Literal, TypedDict, Union, AnyStr
    
    Cross_Origin_Embedder_Policy_Options = TypedDict(
        'Cross_Origin_Embedder_Policy_Options',
        {
            'require-corp': bool,
            'unsafe-none': bool,
            'credentialless': bool,
            'report-to': str
        },
        total=False
    )

    Cross_Origin_Opener_Policy_Options = Literal['same-origin', 'same-origin-allow-popups', 'unsafe-none', 'noopener-allow-popups']

    Cross_Origin_Resource_Policy_Options = Literal['same-origin', 'same-site', 'cross-origin']

    X_Permitted_Cross_Domain_Policies_Options = Literal['none', 'master-only', 'by-content-type', 'by-ftp-filename', 'all', 'none-this-response']

    X_Frame_Options = Literal['SAMEORIGIN', 'DENY']

    X_DNS_Prefetch_Control_Options = Literal['off', 'on']

    Referrer_Policy_Options = list[Literal['no-referrer', 'no-referrer-when-downgrade', 'origin', 'origin-when-cross-origin', 'same-origin', 'strict-origin', 'strict-origin-when-cross-origin', 'unsafe-url']]

    Cache_Control_Options = TypedDict(
        'Cache_Control_Options',
        {
            'max-age': int,
            's-maxage': int,
            'no-cache': bool,
            'no-store': bool,
            'no-transform': bool,
            'must-revalidate': bool,
            'proxy-revalidate': bool,
            'must-understand': bool,
            'private': bool,
            'public': bool,
            'immutable': bool,
            'stale-while-revalidate': int,
            'stale-if-error': int
        },
        total=False
    )

    HSTS_Options = TypedDict(
        'HSTS_Options',
        {
            'max-age': int,
            'includeSubDomains': bool,
            'preload': bool
        },
        total=False
    )

    Content_Security_Policy_Options_Values = list[Union[Literal["'self'", "'none'", "'unsafe-inline'", "'unsafe-eval'", "'trusted-types-eval'", "'strict-dynamic'", "'unsafe-hashes'", "'report-sample'", "'wasm-unsafe-eval'"], AnyStr]]

    Content_Security_Policy_Options = TypedDict(
        'Content_Security_Policy_Options',
        {
            'child-src': Content_Security_Policy_Options_Values,
            'connect-src': Content_Security_Policy_Options_Values,
            'default-src': Content_Security_Policy_Options_Values,
            'font-src': Content_Security_Policy_Options_Values,
            'frame-src': Content_Security_Policy_Options_Values,
            'img-src': Content_Security_Policy_Options_Values,
            'manifest-src': Content_Security_Policy_Options_Values,
            'media-src': Content_Security_Policy_Options_Values,
            'object-src': Content_Security_Policy_Options_Values,
            'script-src': Content_Security_Policy_Options_Values,
            'script-src-elem': Content_Security_Policy_Options_Values,
            'script-src-attr': Content_Security_Policy_Options_Values,
            'style-src': Content_Security_Policy_Options_Values,
            'style-src-elem': Content_Security_Policy_Options_Values,
            'style-src-attr': Content_Security_Policy_Options_Values,
            'worker-src': Content_Security_Policy_Options_Values,
            'base-uri': Content_Security_Policy_Options_Values,
            'sandbox': Content_Security_Policy_Options_Values,
            'form-action': Content_Security_Policy_Options_Values,
            'frame-ancestors': Content_Security_Policy_Options_Values,
            'report-uri': Content_Security_Policy_Options_Values,
            'report-to': Content_Security_Policy_Options_Values,
            'block-all-mixed-content': Content_Security_Policy_Options_Values,
            'require-trusted-types-for': Content_Security_Policy_Options_Values,
            'trusted-types': Content_Security_Policy_Options_Values,
            'upgrade-insecure-requests': Content_Security_Policy_Options_Values,
            'fenced-frame-src': Content_Security_Policy_Options_Values
        },
        total=False
    )

    Permissions_Policy_Options_Values = list[Union[Literal['self', '*'], AnyStr]]

    Permissions_Policy_Options = TypedDict(
        'Permissions_Policy_Options',
        {
            "accelerometer": Permissions_Policy_Options_Values,
            "ambient-light-sensor": Permissions_Policy_Options_Values,
            "aria-notify": Permissions_Policy_Options_Values,
            "attribution-reporting": Permissions_Policy_Options_Values,
            "autoplay": Permissions_Policy_Options_Values,
            "bluetooth": Permissions_Policy_Options_Values,
            "browsing-topics": Permissions_Policy_Options_Values,
            "camera": Permissions_Policy_Options_Values,
            "captured-surface-control": Permissions_Policy_Options_Values,
            "ch-ua-high-entropy-values": Permissions_Policy_Options_Values,
            "compute-pressure": Permissions_Policy_Options_Values,
            "cross-origin-isolated": Permissions_Policy_Options_Values,
            "deferred-fetch": Permissions_Policy_Options_Values,
            "deferred-fetch-minimal": Permissions_Policy_Options_Values,
            "display-capture": Permissions_Policy_Options_Values,
            "encrypted-media": Permissions_Policy_Options_Values,
            "fullscreen": Permissions_Policy_Options_Values,
            "gamepad": Permissions_Policy_Options_Values,
            "geolocation": Permissions_Policy_Options_Values,
            "gyroscope": Permissions_Policy_Options_Values,
            "hid": Permissions_Policy_Options_Values,
            "identity-credentials-get": Permissions_Policy_Options_Values,
            "idle-detection": Permissions_Policy_Options_Values,
            "local-fonts": Permissions_Policy_Options_Values,
            "local-network": Permissions_Policy_Options_Values,
            "local-network-access": Permissions_Policy_Options_Values,
            "loopback-network": Permissions_Policy_Options_Values,
            "magnetometer": Permissions_Policy_Options_Values,
            "microphone": Permissions_Policy_Options_Values,
            "midi": Permissions_Policy_Options_Values,
            "on-device-speech-recognition": Permissions_Policy_Options_Values,
            "otp-credentials": Permissions_Policy_Options_Values,
            "payment": Permissions_Policy_Options_Values,
            "picture-in-picture": Permissions_Policy_Options_Values,
            "private-state-token-issuance": Permissions_Policy_Options_Values,
            "private-state-token-redemption": Permissions_Policy_Options_Values,
            "publickey-credentials-create": Permissions_Policy_Options_Values,
            "publickey-credentials-get": Permissions_Policy_Options_Values,
            "screen-wake-lock": Permissions_Policy_Options_Values,
            "serial": Permissions_Policy_Options_Values,
            "storage-access": Permissions_Policy_Options_Values,
            "summarizer": Permissions_Policy_Options_Values,
            "usb": Permissions_Policy_Options_Values,
            "web-share": Permissions_Policy_Options_Values,
            "window-management": Permissions_Policy_Options_Values,
            "xr-spatial-tracking": Permissions_Policy_Options_Values
        },
        total=False
    )

    Clear_Site_Data_Options = TypedDict(
        'Clear_Site_Data_Options',
        {
            '*': bool,
            'cache': bool,
            'cookies': bool,
            'storage': bool,
            'prefetchCache': bool,
            'prerenderCache': bool,
            'clientHints': bool,
        },
        total=False
    )
    
    SecWeb_Options = TypedDict(
        'SecWeb_Options',
        {
            'csp': Union[Literal[False], Content_Security_Policy_Options],
            'coop': Union[Literal[False], Cross_Origin_Opener_Policy_Options],
            'coep': Union[Literal[False], Cross_Origin_Embedder_Policy_Options],
            'corp': Union[Literal[False], Cross_Origin_Resource_Policy_Options],
            'referrer': Union[Literal[False], Referrer_Policy_Options],
            'xdns': Union[Literal[False], X_DNS_Prefetch_Control_Options],
            'xcdp': Union[Literal[False], X_Permitted_Cross_Domain_Policies_Options],
            'hsts': Union[Literal[False], HSTS_Options],
            'wshsts': Union[Literal[False], HSTS_Options],
            'xframe': Union[Literal[False], X_Frame_Options],
            'permission_policy': Union[Literal[False], Permissions_Policy_Options],
            'cache_control': Union[Literal[False], Cache_Control_Options],
            'xcto': Literal[False],
            'xdo': Literal[False],
            'xss': Literal[False],
            'oac': Literal[False],
        },
        total=False
    )

