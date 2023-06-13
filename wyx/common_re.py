"""
匹配如下手机号
18005551234
1 800 555 1234
+1 800 555-1234
+86 800 555 1234
1-800-555-1234
1 (800) 555-1234
(800)555-1234
(800) 555-1234
(800)5551234
800-555-1234
"""
phone_pattern = r'(?:\+\d+[\s-]*)?(?:\(\d+\)[\s-]*)?(?:\d+[\s-]*)+\d+'