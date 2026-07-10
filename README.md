# EthSwitch Daily Report Generator

A web app for generating IPS, QR, P2P, and POS daily reports.

## Files in this folder
- `app.py` — Main Streamlit web app
- `generate_ips_report.py` — IPS report engine
- `generate_qr_report.py` — QR report engine
- `generate_p2p_report.py` — P2P success rate engine
- `generate_pos_report.py` — POS report engine
- `requirements.txt` — Python dependencies

## How to deploy on Streamlit Cloud (FREE)

1. Create a free account at https://streamlit.io
2. Create a free GitHub account at https://github.com
3. Create a new GitHub repository (e.g. "ethswitch-reports")
4. Upload ALL files in this folder to that repository
5. Go to https://share.streamlit.io
6. Click "New app" → select your repository → set main file as `app.py`
7. Click "Deploy" — your app will be live in ~2 minutes!
8. Share the URL with your colleagues — they just open it in any browser

## How to run locally (on your office computer)

1. Install Python from https://python.org
2. Open Command Prompt and run:
   ```
   pip install streamlit openpyxl pandas
   cd path\to\ethswitch_app
   streamlit run app.py
   ```
3. The app opens automatically in your browser

## Daily usage for colleagues
1. Open the app URL in any browser
2. Select the report tab (IPS / QR / P2P / POS)
3. Choose the report date
4. Upload the required raw file(s)
5. Click Generate — download the formatted Excel report
