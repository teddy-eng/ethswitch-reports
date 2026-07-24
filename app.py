import streamlit as st
import tempfile
import os
import base64
from datetime import date, datetime
from pathlib import Path

from generate_ips_report import generate_report
from generate_qr_report import generate_qr_report
from generate_p2p_report import generate_p2p_report
from generate_pos_report import generate_pos_report
from generate_pos_success_rate_report import generate_pos_success_rate_report

# ── Page config ──
st.set_page_config(
    page_title="CRM Report Hub | EthSwitch S.C.",
    page_icon="🟠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Helper: encode image to base64 ──
def img_to_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

ethswitch_b64 = img_to_b64("ethswitch_logo.png")
ethiopay_b64  = img_to_b64("ethiopay_logo.png")

# ── Global styles ──
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

  html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: #f5f6fa;
  }}

  /* ── Top navbar ── */
  .navbar {{
    background: #0f142a;
    padding: 0.85rem 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 3px solid #f27421;
    margin: -1rem -1rem 0 -1rem;
  }}
  .navbar-left {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
  }}
  .navbar img {{
    height: 38px;
    object-fit: contain;
  }}
  .navbar-divider {{
    width: 1px;
    height: 32px;
    background: rgba(255,255,255,0.2);
  }}
  .navbar-title {{
    font-family: 'Syne', sans-serif;
    font-size: 1.25rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 0.01em;
  }}
  .navbar-title span {{
    color: #f27421;
  }}
  .navbar-badge {{
    background: rgba(242,116,33,0.15);
    border: 1px solid rgba(242,116,33,0.4);
    color: #f27421;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }}

  /* ── Hero strip ── */
  .hero {{
    background: linear-gradient(135deg, #0f142a 0%, #1a2240 60%, #0f142a 100%);
    padding: 2rem 2.5rem 1.8rem;
    margin: 0 -1rem 1.5rem -1rem;
    position: relative;
    overflow: hidden;
  }}
  .hero::before {{
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(242,116,33,0.18) 0%, transparent 70%);
    border-radius: 50%;
  }}
  .hero::after {{
    content: '';
    position: absolute;
    bottom: -30px; left: 30%;
    width: 140px; height: 140px;
    background: radial-gradient(circle, rgba(242,116,33,0.1) 0%, transparent 70%);
    border-radius: 50%;
  }}
  .hero-label {{
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #f27421;
    margin-bottom: 0.4rem;
  }}
  .hero-title {{
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.15;
    margin-bottom: 0.5rem;
  }}
  .hero-sub {{
    font-size: 0.88rem;
    color: rgba(255,255,255,0.55);
    max-width: 520px;
  }}
  .hero-stats {{
    display: flex;
    gap: 2rem;
    margin-top: 1.2rem;
  }}
  .hero-stat {{
    text-align: left;
  }}
  .hero-stat-num {{
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: #f27421;
  }}
  .hero-stat-label {{
    font-size: 0.72rem;
    color: rgba(255,255,255,0.45);
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }}

  /* ── Tab styling ── */
  .stTabs [data-baseweb="tab-list"] {{
    background: #ffffff;
    border-radius: 10px;
    padding: 4px;
    border: 1px solid #e8eaf0;
    gap: 2px;
    box-shadow: 0 1px 4px rgba(15,20,42,0.06);
  }}
  .stTabs [data-baseweb="tab"] {{
    font-size: 0.83rem;
    font-weight: 500;
    color: #6b7280;
    border-radius: 7px;
    padding: 0.45rem 1rem;
    border: none !important;
  }}
  .stTabs [aria-selected="true"] {{
    background: #0f142a !important;
    color: #ffffff !important;
    font-weight: 600;
  }}
  .stTabs [data-baseweb="tab-highlight"] {{
    display: none;
  }}

  /* ── Report cards ── */
  .report-card {{
    background: #ffffff;
    border: 1px solid #e8eaf0;
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    box-shadow: 0 2px 12px rgba(15,20,42,0.05);
    margin-bottom: 1rem;
  }}
  .report-card-title {{
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #0f142a;
    margin-bottom: 0.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }}
  .report-card-sub {{
    font-size: 0.8rem;
    color: #9ca3af;
    margin-bottom: 1.4rem;
  }}
  .accent-dot {{
    width: 8px; height: 8px;
    background: #f27421;
    border-radius: 50%;
    display: inline-block;
  }}

  /* ── Upload zone ── */
  [data-testid="stFileUploader"] {{
    background: #f8f9fc;
    border: 1.5px dashed #d1d5db;
    border-radius: 10px;
    padding: 0.3rem;
    transition: border-color 0.2s;
  }}
  [data-testid="stFileUploader"]:hover {{
    border-color: #f27421;
  }}

  /* ── Buttons ── */
  .stButton > button {{
    background: #0f142a !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.02em !important;
    transition: background 0.2s, transform 0.1s !important;
    box-shadow: 0 2px 8px rgba(15,20,42,0.18) !important;
  }}
  .stButton > button:hover {{
    background: #f27421 !important;
    transform: translateY(-1px) !important;
  }}

  /* ── Download button ── */
  [data-testid="stDownloadButton"] > button {{
    background: #f27421 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    box-shadow: 0 2px 8px rgba(242,116,33,0.3) !important;
  }}
  [data-testid="stDownloadButton"] > button:hover {{
    background: #d9661a !important;
  }}

  /* ── Date input ── */
  [data-testid="stDateInput"] input {{
    border-radius: 8px !important;
    border-color: #e8eaf0 !important;
    font-size: 0.88rem !important;
  }}

  /* ── Success / Error ── */
  [data-testid="stAlert"] {{
    border-radius: 9px !important;
    font-size: 0.85rem !important;
  }}

  /* ── Footer ── */
  .footer {{
    background: #0f142a;
    color: rgba(255,255,255,0.35);
    text-align: center;
    font-size: 0.75rem;
    padding: 1rem;
    margin: 2rem -1rem -1rem -1rem;
    border-top: 2px solid #f27421;
    letter-spacing: 0.04em;
  }}
  .footer span {{ color: #f27421; }}

  /* Hide Streamlit branding */
  #MainMenu, footer, header {{ visibility: hidden; }}
  .block-container {{ padding-top: 0 !important; max-width: 860px; }}
</style>

<!-- Navbar -->
<div class="navbar">
  <div class="navbar-left">
    {"<img src='data:image/png;base64," + ethswitch_b64 + "' />" if ethswitch_b64 else ""}
    <div class="navbar-divider"></div>
    {"<img src='data:image/png;base64," + ethiopay_b64 + "' />" if ethiopay_b64 else ""}
    <div class="navbar-divider"></div>
    <div class="navbar-title">CRM <span>Report Hub</span></div>
  </div>
  <div class="navbar-badge">CRM Division</div>
</div>

<!-- Hero -->
<div class="hero">
  <div class="hero-label">EthSwitch S.C. — Client Relationship Management</div>
  <div class="hero-title">Daily Transaction<br>Report Generator</div>
  <div class="hero-sub">Upload your raw SmartVista data and download formatted executive reports in seconds — no manual work needed.</div>
  <div class="hero-stats">
    <div class="hero-stat">
      <div class="hero-stat-num">5</div>
      <div class="hero-stat-label">Report Types</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-num">IPS · QR · POS</div>
      <div class="hero-stat-label">Payment Channels</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-num">Auto</div>
      <div class="hero-stat-label">FI Detection</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Helpers ──
def save_upload(uploaded_file):
    suffix = os.path.splitext(uploaded_file.name)[1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.read())
    tmp.close()
    return tmp.name

def download_button(output_path, filename):
    with open(output_path, "rb") as f:
        st.download_button(
            label="⬇️  Download Report",
            data=f,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

def card_header(icon, title, subtitle):
    st.markdown(f"""
    <div class="report-card-title"><span class="accent-dot"></span>{icon} {title}</div>
    <div class="report-card-sub">{subtitle}</div>
    """, unsafe_allow_html=True)

# ── Tabs ──
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  IPS Report",
    "📷  QR Report",
    "📈  P2P Success Rate",
    "🖥️  POS Report",
    "✅  POS Success Rate",
])

# ══════════════════════════════
# TAB 1 — IPS
# ══════════════════════════════
with tab1:
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    card_header("📊", "IPS Successful Transaction Report",
                "Interoperable Payment System — daily source & destination breakdown by FI")
    report_date = st.date_input("Report date", value=date.today(), key="ips_date")
    ips_file = st.file_uploader("Upload IPS success file (.xlsx)", type=["xlsx"], key="ips_file")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Generate IPS Report", use_container_width=True, key="btn_ips"):
        if not ips_file:
            st.error("Please upload the IPS success file.")
        else:
            with st.spinner("Generating report..."):
                try:
                    input_path = save_upload(ips_file)
                    out_name = f"Successful IPS Transaction for {report_date.strftime('%B')} {report_date.day},{report_date.year}.xlsx"
                    output_path = os.path.join(tempfile.gettempdir(), out_name)
                    generate_report(input_path, output_path, datetime.combine(report_date, datetime.min.time()))
                    st.success("✅ Report generated successfully!")
                    download_button(output_path, out_name)
                except Exception as e:
                    st.error(f"Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════
# TAB 2 — QR
# ══════════════════════════════
with tab2:
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    card_header("📷", "QR Successful Transaction Report",
                "EthioPay QR — daily interoperable QR transaction summary by FI")
    report_date_qr = st.date_input("Report date", value=date.today(), key="qr_date")
    qr_file = st.file_uploader("Upload QR success file (.xlsx)", type=["xlsx"], key="qr_file")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Generate QR Report", use_container_width=True, key="btn_qr"):
        if not qr_file:
            st.error("Please upload the QR success file.")
        else:
            with st.spinner("Generating report..."):
                try:
                    input_path = save_upload(qr_file)
                    out_name = f"Successful QR Transaction for {report_date_qr.strftime('%B')} {report_date_qr.day},{report_date_qr.year}.xlsx"
                    output_path = os.path.join(tempfile.gettempdir(), out_name)
                    generate_qr_report(input_path, output_path, datetime.combine(report_date_qr, datetime.min.time()))
                    st.success("✅ Report generated successfully!")
                    download_button(output_path, out_name)
                except Exception as e:
                    st.error(f"Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════
# TAB 3 — P2P Success Rate
# ══════════════════════════════
with tab3:
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    card_header("📈", "IPS-P2P Success Rate Report",
                "Color-coded success rate per FI — Green ≥98.7% · Yellow 96–98.7% · Red ≤96%")
    report_date_p2p = st.date_input("Report date", value=date.today(), key="p2p_date")
    col1, col2 = st.columns(2)
    with col1:
        error_file = st.file_uploader("Decline / Error file (.xlsx)", type=["xlsx"], key="p2p_error")
    with col2:
        success_file_p2p = st.file_uploader("IPS Success file (.xlsx)", type=["xlsx"], key="p2p_success")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Generate P2P Report", use_container_width=True, key="btn_p2p"):
        if not error_file or not success_file_p2p:
            st.error("Please upload both files.")
        else:
            with st.spinner("Generating report..."):
                try:
                    error_path   = save_upload(error_file)
                    success_path = save_upload(success_file_p2p)
                    out_name = f"IPS-P2P Success Rate Report for {report_date_p2p.strftime('%B')} {report_date_p2p.day},{report_date_p2p.year}.xlsx"
                    output_path = os.path.join(tempfile.gettempdir(), out_name)
                    generate_p2p_report(error_path, success_path, output_path, datetime.combine(report_date_p2p, datetime.min.time()))
                    st.success("✅ Report generated successfully!")
                    download_button(output_path, out_name)
                except Exception as e:
                    st.error(f"Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════
# TAB 4 — POS Report
# ══════════════════════════════
with tab4:
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    card_header("🖥️", "POS Successful With Value Report",
                "Point of Sale — successful purchase transactions as Issuer & Acquirer")
    report_date_pos = st.date_input("Report date", value=date.today(), key="pos_date")
    col3, col4 = st.columns(2)
    with col3:
        issuer_file = st.file_uploader("Issuer file (.xlsx)", type=["xlsx"], key="pos_issuer")
    with col4:
        acquirer_file = st.file_uploader("Acquirer file (.xlsx)", type=["xlsx"], key="pos_acquirer")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Generate POS Report", use_container_width=True, key="btn_pos"):
        if not issuer_file or not acquirer_file:
            st.error("Please upload both Issuer and Acquirer files.")
        else:
            with st.spinner("Generating report..."):
                try:
                    issuer_path   = save_upload(issuer_file)
                    acquirer_path = save_upload(acquirer_file)
                    out_name = f"POS Successful With Value {report_date_pos.strftime('%B')} {report_date_pos.day},{report_date_pos.year}.xlsx"
                    output_path = os.path.join(tempfile.gettempdir(), out_name)
                    generate_pos_report(issuer_path, acquirer_path, output_path, datetime.combine(report_date_pos, datetime.min.time()))
                    st.success("✅ Report generated successfully!")
                    download_button(output_path, out_name)
                except Exception as e:
                    st.error(f"Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════
# TAB 5 — POS Success Rate
# ══════════════════════════════
with tab5:
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    card_header("✅", "POS Success Rate Report",
                "POS transaction success rate analysis from SmartVista raw export")
    report_date_posr = st.date_input("Report date", value=date.today(), key="posr_date")
    posr_file = st.file_uploader("Upload SmartVista POS raw transaction export (.xlsx)", type=["xlsx"], key="posr_file")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Generate POS Success Rate Report", use_container_width=True, key="btn_posr"):
        if not posr_file:
            st.error("Please upload the raw POS transaction export.")
        else:
            with st.spinner("Generating report..."):
                try:
                    input_path = save_upload(posr_file)
                    out_name = f"POS SUCCESS RATE {report_date_posr.strftime('%B')} {report_date_posr.day},{report_date_posr.year}.xlsx"
                    output_path = os.path.join(tempfile.gettempdir(), out_name)
                    unknown_codes, unmapped_issuers = generate_pos_success_rate_report(
                        input_path, output_path, datetime.combine(report_date_posr, datetime.min.time())
                    )
                    st.success("✅ Report generated successfully!")
                    if unknown_codes:
                        st.warning(f"New response code(s) found: {unknown_codes}")
                    if unmapped_issuers:
                        st.warning(f"New bank(s) found: {unmapped_issuers}")
                    download_button(output_path, out_name)
                except Exception as e:
                    st.error(f"Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div class="footer">
  <span>CRM Report Hub</span> &nbsp;·&nbsp; EthSwitch S.C. &nbsp;·&nbsp; Client Relationship Management Division &nbsp;·&nbsp; Powered by EthioPay
</div>
""", unsafe_allow_html=True)
