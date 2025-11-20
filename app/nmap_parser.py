
from typing import List, Dict, Any

def parse_scan_file(raw_bytes: bytes) -> List[Dict[str, Any]]:
    text = raw_bytes.decode(errors="ignore")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    records: List[Dict[str, Any]] = []

    if not lines:
        return records

    if lines[0].lower().startswith("host,"):
        data_lines = lines[1:]
    else:
        data_lines = lines

    for line in data_lines:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 4:
            continue
        host, port, service, version = parts[:4]
        records.append({
            "host": host,
            "port": port,
            "service": service,
            "version": version,
        })

    return records
