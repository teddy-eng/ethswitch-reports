import streamlit as st
import tempfile
import os
import base64
from datetime import date, datetime

from generate_ips_report import generate_report
from generate_qr_report import generate_qr_report
from generate_p2p_report import generate_p2p_report
from generate_pos_report import generate_pos_report
from generate_pos_success_rate_report import generate_pos_success_rate_report

st.set_page_config(
    page_title="CRM Report Hub | EthSwitch S.C.",
    page_icon="🟠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def img_to_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

ethswitch_b64 = img_to_b64("ethswitch_logo.png")
ethiopay_b64  = img_to_b64("ethiopay_logo.png")

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

  html, body, [class*="css"],
  [data-testid="stAppViewContainer"],
  [data-testid="stMain"],
  .main, .block-container {{
    font-family: 'Inter', sans-serif;
    background-color: #0f142a !important;
    color: #ffffff !important;
  }}

  /* ── Navbar ── */
  .navbar {{
    background: #0f142a;
    padding: 1rem 2rem;
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    border-bottom: 3px solid #f27421;
    margin: -1rem -1rem 0 -1rem;
  }}
  .navbar-left {{ display:flex; align-items:center; justify-content:flex-start; }}
  .navbar-left img {{ height:60px; object-fit:contain; }}
  .navbar-center {{ display:flex; flex-direction:column; align-items:center; }}
  .navbar-app-name {{
    font-family:'Syne',sans-serif;
    font-size:1.6rem; font-weight:800;
    color:#f27421; white-space:nowrap;
  }}
  .navbar-right {{ display:flex; align-items:center; justify-content:flex-end; }}
  .navbar-right img {{ height:60px; object-fit:contain; }}

  /* ── Hero ── */
  .hero {{
    background:linear-gradient(135deg,#0f142a 0%,#1a2240 60%,#0f142a 100%);
    padding:1.5rem 2.5rem;
    margin:0 -1rem 1.5rem -1rem;
    border-bottom:1px solid rgba(242,116,33,0.2);
    text-align:center;
  }}
  .hero-title {{
    font-family:'Syne',sans-serif;
    font-size:1.5rem; font-weight:800;
    color:#f27421; letter-spacing:0.05em;
    text-transform:uppercase;
  }}
  .hero-sub {{ font-size:0.85rem; color:rgba(255,255,255,0.45); margin-top:0.3rem; }}

  /* ── Custom Tabs ── */
  .custom-tabs {{
    display:flex; gap:6px; flex-wrap:wrap;
    background:#1a2240;
    padding:6px; border-radius:10px;
    border:1px solid rgba(242,116,33,0.2);
    margin-bottom:1rem;
  }}
  .custom-tab {{
    padding:8px 16px;
    border-radius:7px;
    font-size:0.88rem; font-weight:800;
    cursor:pointer;
    background:#0f142a;
    color:#f27421 !important;
    border:1.5px solid #f27421;
    transition:all 0.2s;
    white-space:nowrap;
    letter-spacing:0.02em;
  }}
  .custom-tab:hover {{
    background:#f27421;
    color:#ffffff !important;
  }}
  .custom-tab.active {{
    background:#f27421 !important;
    color:#ffffff !important;
    border:1.5px solid #f27421;
  }}

  /* ── Report cards ── */
  .report-card {{
    background:#1a2240;
    border:1px solid rgba(242,116,33,0.2);
    border-radius:14px;
    padding:1.6rem 1.8rem;
    margin-bottom:1rem;
  }}
  .report-card-title {{
    font-family:'Syne',sans-serif;
    font-size:1.1rem; font-weight:800;
    color:#f27421; margin-bottom:0.2rem;
  }}
  .report-card-sub {{
    font-size:0.82rem; color:rgba(255,255,255,0.4);
    margin-bottom:1.4rem;
    border-left:3px solid #f27421; padding-left:0.6rem;
  }}

  /* ── Upload label ── */
  .upload-label {{
    font-size:0.82rem; font-weight:700;
    color:#f27421; text-transform:uppercase;
    letter-spacing:0.07em; margin-bottom:4px;
  }}

  /* ── Date label ── */
  [data-testid="stDateInput"] label {{
    color:#f27421 !important; font-weight:700 !important;
    font-size:0.85rem !important; text-transform:uppercase !important;
    letter-spacing:0.07em !important;
  }}
  [data-testid="stDateInput"] input {{
    background:#0f142a !important; color:#ffffff !important;
    border:1px solid rgba(242,116,33,0.3) !important;
    border-radius:8px !important;
  }}

  /* ── File uploader — force green Upload button ── */
  [data-testid="stFileUploader"] {{
    background:#0f142a !important;
    border:1.5px dashed rgba(242,116,33,0.4) !important;
    border-radius:10px !important;
  }}
  [data-testid="stFileUploaderDropzone"] {{
    background:#0f142a !important;
  }}
  [data-testid="stFileUploader"] button,
  [data-testid="stFileUploaderDropzoneInstructions"] button,
  [data-testid="stBaseButton-secondary"] {{
    background:#00b050 !important;
    color:#ffffff !important;
    border:none !important;
    border-radius:6px !important;
    font-weight:700 !important;
  }}
  [data-testid="stFileUploader"] span,
  [data-testid="stFileUploader"] p,
  [data-testid="stFileUploader"] small {{
    color:rgba(255,255,255,0.7) !important;
  }}

  /* ── Main buttons ── */
  .stButton > button {{
    background:#f27421 !important; color:#ffffff !important;
    border:none !important; border-radius:9px !important;
    padding:0.6rem 1.5rem !important; font-weight:700 !important;
    font-size:0.9rem !important;
    box-shadow:0 2px 12px rgba(242,116,33,0.3) !important;
  }}
  .stButton > button:hover {{
    background:#d9661a !important; transform:translateY(-1px) !important;
  }}

  /* ── Download button ── */
  [data-testid="stDownloadButton"] > button {{
    background:#0f142a !important; color:#ffffff !important;
    border:1.5px solid #f27421 !important; border-radius:9px !important;
    font-weight:700 !important;
  }}
  [data-testid="stDownloadButton"] > button:hover {{
    background:#f27421 !important;
  }}

  /* ── Footer ── */
  .footer {{
    background:#0f142a; border-top:2px solid #f27421;
    text-align:center; padding:1rem;
    margin:2rem -1rem -1rem -1rem;
    font-size:0.8rem; color:rgba(255,255,255,0.45);
    letter-spacing:0.04em;
  }}
  .footer span {{ color:#f27421; font-weight:600; }}

  #MainMenu, footer, header {{ visibility:hidden; }}
  .block-container {{ padding-top:0 !important; max-width:900px; }}
</style>

<!-- Navbar -->
<div class="navbar">
  <div class="navbar-left">
    {"<img src='data:image/png;base64," + ethswitch_b64 + "' />" if ethswitch_b64 else ""}
  </div>
  <div class="navbar-center">
    <div class="navbar-app-name">CRM Report Hub</div>
  </div>
  <div class="navbar-right">
    {"<img src='data:image/png;base64," + ethiopay_b64 + "' />" if ethiopay_b64 else ""}
  </div>
</div>

<!-- Hero -->
<div class="hero">
  <div class="hero-title">Daily Report Generator</div>
  <div class="hero-sub">Upload your raw SmartVista data and download formatted Reports</div>
</div>
""", unsafe_allow_html=True)

# ── Custom tab state ──
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "IPS"

tabs_def = [
    ("IPS",  "💳  IPS Report"),
    ("QR",   "⬛  QR Report"),
    ("P2P",  "🔄  P2P Success Rate"),
    ("POS",  "🏪  POS Report"),
    ("POSR", "✅  POS Success Rate"),
]

# ── Render custom tab bar ──
tab_html = '<div class="custom-tabs">'
for key, label in tabs_def:
    active_class = "active" if st.session_state.active_tab == key else ""
    tab_html += f'<div class="custom-tab {active_class}" onclick="selectTab(\'{key}\')">{label}</div>'
tab_html += "</div>"

tab_html += """
<script>
function selectTab(key) {
  // Use Streamlit's setComponentValue via query param trick
  const url = new URL(window.location);
  url.searchParams.set('tab', key);
  window.history.replaceState({}, '', url);
  // Find and click the hidden radio
  const radios = window.parent.document.querySelectorAll('input[type=radio]');
  radios.forEach(r => { if(r.value === key) r.click(); });
}
</script>
"""
st.markdown(tab_html, unsafe_allow_html=True)

# ── Use radio for actual tab switching (hidden) ──
st.markdown("<style>div[data-testid='stRadio']{display:none}</style>", unsafe_allow_html=True)
active = st.radio("tab", [k for k, _ in tabs_def], key="active_tab", label_visibility="collapsed")

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
            data=f, file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

def card_header(title, subtitle):
    st.markdown(f'<div class="report-card-title">{title}</div>'
                f'<div class="report-card-sub">{subtitle}</div>',
                unsafe_allow_html=True)

def upload_label(text):
    st.markdown(f'<div class="upload-label">{text}</div>', unsafe_allow_html=True)

# ══════════════════════════════
# IPS
# ══════════════════════════════
if active == "IPS":
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    card_header("💳 IPS Successful Transaction Report",
                "Source & destination breakdown by FI — sorted A to Z with totals")
    report_date = st.date_input("Report Date", value=date.today(), key="ips_date")
    upload_label("IPS Success File")
    ips_file = st.file_uploader("IPS success file (.xlsx)", type=["xlsx"], key="ips_file", label_visibility="collapsed")
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
# QR
# ══════════════════════════════
elif active == "QR":
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    card_header("⬛ QR Successful Transaction Report",
                "EthioPay QR interoperable transactions — sorted A to Z with totals")
    report_date_qr = st.date_input("Report Date", value=date.today(), key="qr_date")
    upload_label("QR Success File")
    qr_file = st.file_uploader("QR success file (.xlsx)", type=["xlsx"], key="qr_file", label_visibility="collapsed")
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
# P2P
# ══════════════════════════════
elif active == "P2P":
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    card_header("🔄 IPS-P2P Success Rate Report",
                "Color-coded success rate per FI — Green ≥98.7% · Yellow 96–98.7% · Red ≤96%")
    report_date_p2p = st.date_input("Report Date", value=date.today(), key="p2p_date")
    col1, col2 = st.columns(2)
    with col1:
        upload_label("Decline / Error Report")
        error_file = st.file_uploader("Decline file", type=["xlsx"], key="p2p_error", label_visibility="collapsed")
    with col2:
        upload_label("IPS Success Report")
        success_file_p2p = st.file_uploader("Success file", type=["xlsx"], key="p2p_success", label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Generate P2P Report", use_container_width=True, key="btn_p2p"):
        if not error_file or not success_file_p2p:
            st.error("Please upload both the Decline/Error report and the IPS Success report.")
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
# POS
# ══════════════════════════════
elif active == "POS":
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    card_header("🏪 POS Successful With Value Report",
                "Point of Sale — successful purchase transactions as Issuer & Acquirer")
    report_date_pos = st.date_input("Report Date", value=date.today(), key="pos_date")
    col3, col4 = st.columns(2)
    with col3:
        upload_label("Issuer Report")
        issuer_file = st.file_uploader("Issuer file", type=["xlsx"], key="pos_issuer", label_visibility="collapsed")
    with col4:
        upload_label("Acquirer Report")
        acquirer_file = st.file_uploader("Acquirer file", type=["xlsx"], key="pos_acquirer", label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Generate POS Report", use_container_width=True, key="btn_pos"):
        if not issuer_file or not acquirer_file:
            st.error("Please upload both the Issuer and Acquirer reports.")
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
# POS Success Rate
# ══════════════════════════════
elif active == "POSR":
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    card_header("✅ POS Success Rate Report",
                "POS transaction success rate analysis from SmartVista raw export")
    report_date_posr = st.date_input("Report Date", value=date.today(), key="posr_date")
    upload_label("SmartVista POS Raw Transaction Export")
    posr_file = st.file_uploader("POS raw export", type=["xlsx"], key="posr_file", label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Generate POS Success Rate Report", use_container_width=True, key="btn_posr"):
        if not posr_file:
            st.error("Please upload the SmartVista POS raw transaction export.")
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
  <span>EthSwitch S.C.</span> &nbsp;|&nbsp; Powered By: <span>CRM Department</span> &nbsp;|&nbsp; © 2026
</div>
""", unsafe_allow_html=True)
