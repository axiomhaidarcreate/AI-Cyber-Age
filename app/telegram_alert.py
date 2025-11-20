
import os
from typing import Dict, Any
import requests

TELEGRAM_TOKEN = os.getenv("AGENT_TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("AGENT_TELEGRAM_CHAT_ID")

def send_telegram_alert(finding: Dict[str, Any]) -> None:
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return

    msg = (
        "\u26a0\ufe0f AI Cyber Agent Alert\n"
        f"Host: {finding.get('host')}\n"
        f"Port: {finding.get('port')} ({finding.get('service')})\n"
        f"Issue: {finding.get('issue_type')}\n"
        f"Risk: {finding.get('risk')} (score {finding.get('risk_score')})"
    )

    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={"chat_id": TELEGRAM_CHAT_ID, "text": msg},
            timeout=5,
        )
    except Exception:
        pass
