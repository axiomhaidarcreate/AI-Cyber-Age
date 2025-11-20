
from typing import List, Dict, Any
import pandas as pd
import re

SERVICE_MAP = {
    "ssh": 1,
    "telnet": 2,
    "http": 3,
    "https": 4,
    "ftp": 5,
    "smb": 6,
    "mysql": 7,
    "dns": 8,
}

def parse_version_number(version: str) -> float:
    if not version:
        return 0.0
    nums = re.findall(r"[0-9]+(?:\.[0-9]+)?", version)
    if not nums:
        return 0.0
    try:
        return float(nums[0])
    except ValueError:
        return 0.0

def build_feature_frame(records: List[Dict[str, Any]]) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()

    rows = []
    for rec in records:
        service = (rec.get("service") or "").lower()
        version = rec.get("version") or ""
        port = int(rec.get("port") or 0)

        service_code = SERVICE_MAP.get(service, 0)
        version_num = parse_version_number(version)
        is_plaintext = 1 if service in ("ftp", "telnet", "http") else 0

        rows.append({
            "port": port,
            "service_code": service_code,
            "version_num": version_num,
            "is_plaintext": is_plaintext,
        })

    return pd.DataFrame(rows)
