import re
import sqlite3

FORBIDDEN_KEYWORDS = re.compile(
    r"\b(DROP|DELETE|UPDATE|INSERT|ALTER|TRUNCATE|ATTACH|DETACH|PRAGMA|REPLACE)\b",
    re.IGNORECASE,
)

def validate_readonly_sql(sql: str) -> tuple[bool, str]:
    cleaned = sql.strip().rstrip(";")
    if not cleaned.upper().startswith(("SELECT", "WITH")):
        return False, "Blocked: Only SELECT or CTE (WITH) queries are permitted."
    if ";" in cleaned:
        return False, "Blocked: Stacked multi-statement SQL queries are forbidden."
    match = FORBIDDEN_KEYWORDS.search(cleaned)
    if match:
        return False, f"Blocked: Forbidden DDL/DML keyword detected ({match.group(0).upper()})."
    return True, "Valid read-only query."

def execute_safe_query(db_path: str, sql: str) -> dict:
    is_safe, reason = validate_readonly_sql(sql)
    if not is_safe:
        return {"status": "rejected", "error": reason, "rows": []}

    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        rows = [dict(r) for r in conn.execute(sql).fetchall()]
        return {"status": "success", "row_count": len(rows), "rows": rows}
    except sqlite3.Error as exc:
        return {"status": "sql_error", "error": str(exc), "rows": []}
    finally:
        conn.close()
