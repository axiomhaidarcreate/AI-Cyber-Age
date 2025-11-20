
# AI Cyber Agent – Tinker-Ready (Defensive, Automated)

This project is a **defensive-only** AI-assisted cyber agent that:
- Accepts *existing* scan results (e.g., from Nmap) as files
- Parses and converts them into features
- Runs a pre-trained ML model (that **you** provide) to estimate risk
- Stores results in a local SQLite database
- Exposes a FastAPI backend for automation & integration
- Provides a Streamlit dashboard for users
- Can optionally send Telegram alerts using environment variables

⚠️ **Important**
- This project does **not** perform any active scanning by itself.
- You (or your infrastructure) are responsible for running Nmap or any scanner you own, on networks you are authorized to assess.
- The agent only processes scan *outputs* for defensive analysis.

## Components

- `app/agent.py` – Core analysis logic (loads model + rules).
- `app/feature_extractor.py` – Turns parsed scan data into ML features.
- `app/nmap_parser.py` – Safe placeholder parser for scan files.
- `app/db.py` – SQLite database helper.
- `app/telegram_alert.py` – Optional Telegram alert integration.
- `app/api.py` – FastAPI backend (for Tinker Machine AI backend service).
- `app/dashboard.py` – Streamlit dashboard (for Tinker frontend app).
- `requirements.txt` – Python dependencies.

## How to Use (Locally)

Install dependencies:

```bash
pip install -r requirements.txt
```

Run backend API:

```bash
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

Run dashboard:

```bash
streamlit run app/dashboard.py
```

Then open the Streamlit URL in your browser and upload a scan file.

## Model Integration

Edit `app/agent.py`:

- Point `MODEL_PATH` to your `.pkl` model file.
- Implement your real feature pipeline in `feature_extractor.py`.

## Tinker Machine AI

On Tinker:
- Deploy `api.py` as a backend service.
- Deploy `dashboard.py` as a frontend Streamlit app.
- Configure the dashboard to point to the API URL.
