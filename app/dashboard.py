
import streamlit as st
import requests
import os

API_URL = os.getenv("AGENT_API_URL", "http://localhost:8000")

st.set_page_config(page_title="AI Cyber Agent", layout="wide")
st.title("AI Cyber Agent – Network Vulnerability & Misconfiguration Viewer")

st.markdown(
    "هذه الأداة دفاعية فقط، تقوم بتحليل نتائج فحص الشبكة "
    "التي ترفعها أنت (مثل مخرجات Nmap بصيغة CSV: host,port,service,version)."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1️⃣ رفع نتيجة فحص لتحليلها")
    upload = st.file_uploader("ارفع ملف فحص (CSV)", type=["csv", "txt"])
    if upload is not None:
        with st.spinner("يتم إرسال الملف إلى الوكيل لتحليله..."):
            try:
                resp = requests.post(
                    f"{API_URL}/analyze",
                    files={"file": (upload.name, upload.getvalue())},
                    timeout=30,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    st.success("تم التحليل بنجاح ✅")
                    findings = data.get("findings", [])
                    st.subheader("ملخص:")
                    st.json(
                        {
                            "total": data.get("total"),
                            "high_or_critical": data.get("high_or_critical"),
                            "by_issue_type": data.get("by_issue_type"),
                        }
                    )
                    if findings:
                        st.subheader("النتائج التفصيلية")
                        st.dataframe(findings)
                else:
                    st.error(f"فشل التحليل: {resp.status_code} - {resp.text}")
            except Exception as e:
                st.error(f"خطأ في الاتصال بالـ API: {e}")

with col2:
    st.subheader("2️⃣ آخر النتائج المخزّنة في قاعدة البيانات")
    if st.button("تحديث التقارير"):
        try:
            resp = requests.get(f"{API_URL}/reports/latest?limit=50", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                st.write(f"عدد النتائج: {data.get('count')}")
                if data.get("items"):
                    st.dataframe(data["items"])
                else:
                    st.info("لا توجد نتائج بعد.")
            else:
                st.error(f"فشل جلب التقارير: {resp.status_code}")
        except Exception as e:
            st.error(f"خطأ في الاتصال بالـ API: {e}")

st.markdown("---")
st.caption("AI Cyber Agent – Defensive, read-only analysis only.")
