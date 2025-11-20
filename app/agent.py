
import os
from typing import List, Dict, Any, Optional
import joblib

from .feature_extractor import build_feature_frame
from . import db
from .telegram_alert import send_telegram_alert

MODEL_PATH = os.getenv("AGENT_MODEL_PATH", "model/model.pkl")
_model = None

def load_model() -> Optional[Any]:
    global _model
    if _model is not None:
        return _model
    if not os.path.exists(MODEL_PATH):
        return None
    _model = joblib.load(MODEL_PATH)
    return _model

def simple_risk_heuristic(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results = []
    for rec in records:
        service = (rec.get("service") or "").lower()
        version = (rec.get("version") or "").lower()
        port = int(rec.get("port") or 0)

        risk = "low"
        score = 1.0
        issue_type = "info"

        if "smbv1" in version:
            risk, score, issue_type = "critical", 9.0, "vulnerability"
        elif service == "telnet":
            risk, score, issue_type = "high", 7.5, "misconfiguration"
        elif service == "ftp" and "tls" not in version:
            risk, score, issue_type = "high", 7.0, "misconfiguration"
        elif service == "http" and port == 80:
            risk, score, issue_type = "medium", 5.0, "misconfiguration"
        elif "openssh" in version and "7.2" in version:
            risk, score, issue_type = "medium", 4.5, "vulnerability"

        result = {
            **rec,
            "risk": risk,
            "risk_score": score,
            "issue_type": issue_type,
        }
        results.append(result)
    return results

def analyze_scan(parsed_scan: List[Dict[str, Any]]) -> Dict[str, Any]:
    model = load_model()
    features_df = build_feature_frame(parsed_scan)

    if model is not None and not features_df.empty:
        preds = model.predict(features_df)
        results = []
        for rec, label in zip(parsed_scan, preds):
            issue_type = "none"
            risk = "low"
            score = 0.0
            if label == 1:
                issue_type = "vulnerability"
                risk, score = "high", 8.0
            elif label == 2:
                issue_type = "misconfiguration"
                risk, score = "medium", 5.0

            results.append({
                **rec,
                "issue_type": issue_type,
                "risk": risk,
                "risk_score": score,
                "model_label": int(label),
            })
    else:
        results = simple_risk_heuristic(parsed_scan)

    for r in results:
        db.save_finding(r)
        if r.get("risk") in ("high", "critical"):
            send_telegram_alert(r)

    summary = {
        "total": len(results),
        "high_or_critical": sum(1 for r in results if r["risk"] in ("high", "critical")),
        "by_issue_type": {},
        "findings": results,
    }

    for r in results:
        issue_type = r.get("issue_type") or "none"
        summary["by_issue_type"][issue_type] = summary["by_issue_type"].get(issue_type, 0) + 1

    return summary
