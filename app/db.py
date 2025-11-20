
import os
import sqlite3
from typing import Dict, Any, List
from datetime import datetime

DB_PATH = os.getenv("AGENT_DB_PATH", "data/agent.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT,
            host TEXT,
            port INTEGER,
            service TEXT,
            version TEXT,
            issue_type TEXT,
            risk TEXT,
            risk_score REAL
        )"""
    )
    conn.commit()
    conn.close()

def save_finding(rec: Dict[str, Any]):
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO findings (ts, host, port, service, version, issue_type, risk, risk_score)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            datetime.utcnow().isoformat(),
            rec.get("host"),
            int(rec.get("port") or 0),
            rec.get("service"),
            rec.get("version"),
            rec.get("issue_type"),
            rec.get("risk"),
            float(rec.get("risk_score") or 0.0),
        )
    )
    conn.commit()
    conn.close()

def list_findings(limit: int = 100) -> List[dict]:
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT ts, host, port, service, version, issue_type, risk, risk_score FROM findings ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
