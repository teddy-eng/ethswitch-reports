import streamlit as st
import tempfile
import os
from datetime import date

from generate_ips_report import generate_report
from generate_qr_report import generate_qr_report
from generate_p2p_report import generate_p2p_report
from generate_pos_report import generate_pos_report
from generate_pos_success_rate_report import generate_pos_success_rate_report

st.set_page_config(
    page_title="EthSwitch Report Generator",
    page_icon="📊",
    layout="centered"
)

st.markdown("""
<style>
.header-box {
    background-color: #1a5276;
    padding: 1.2rem 1.5rem;
    border-radius: 10px;
    margin-bottom: 1.5rem;
}
.header-box h1 { color: white; font-size: 1.5rem; margin: 0; }
.header-box p { color: #aed6f1; font-size: 0.9rem; margin: 0.3rem 0 0; }
.stTabs [data-baseweb="tab"] { font-size: 0.95rem; font-weight: 500; }
</style>
<div class="header-box">
<h1>📊 EthSwitch S.C. — Daily Report Generator</h1>
<p>Upload your raw data files and download the formatted executive report instantly.</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["IPS Report", "QR Report", "P2P Success Rate", "POS Report", "POS Success Rate"]
)

# ── Helper ──
def save_upload(uploaded_file):
    suffix = os.path.splitext(uploaded_file.name)[1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.read())
    tmp.close()
    return tmp.name

def download_button(output_path, filename):
    with open(output_path, "rb") as f:
        st.download_button(
            label="⬇️ Download Report",
            data=f,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

# ══════════════════════════════
# TAB 1 — IPS Report
# ══════════════════════════════
with tab1:
    st.subheader("IPS Successful Transaction Report")
    report_date = st.date_input("Report date", value=date.today(), key="ips_date")
    ips_file = st.file_uploader("Upload IPS success file (.xlsx)", type=["xlsx"], key="ips_file")

    if st.button("Generate IPS Report", use_container_width=True, key="btn_ips"):
        if not ips_file:
            st.error("Please upload the IPS success file.")
        else:
            with st.spinner("Generating report..."):
                try:
                    input_path = save_upload(ips_file)
                    out_name = f"Successful_IPS_Transaction_for_{report_date.strftime('%B_%d_%Y')}.xlsx"
                    output_path = os.path.join(tempfile.gettempdir(), out_name)
                    from datetime import datetime
                    generate_report(input_path, output_path, datetime.combine(report_date, datetime.min.time()))
                    st.success("✅ Report generated successfully!")
                    download_button(output_path, out_name)
                except Exception as e:
                    st.error(f"Error: {e}")

# ══════════════════════════════
# TAB 2 — QR Report
# ══════════════════════════════
with tab2:
    st.subheader("QR Successful Transaction Report")
    report_date_qr = st.date_input("Report date", value=date.today(), key="qr_date")
    qr_file = st.file_uploader("Upload QR success file (.xlsx)", type=["xlsx"], key="qr_file")

    if st.button("Generate QR Report", use_container_width=True, key="btn_qr"):
        if not qr_file:
            st.error("Please upload the QR success file.")
        else:
            with st.spinner("Generating report..."):
                try:
                    input_path = save_upload(qr_file)
                    out_name = f"Successful_QR_Transaction_for_{report_date_qr.strftime('%B_%d_%Y')}.xlsx"
                    output_path = os.path.join(tempfile.gettempdir(), out_name)
                    from datetime import datetime
                    generate_qr_report(input_path, output_path, datetime.combine(report_date_qr, datetime.min.time()))
                    st.success("✅ Report generated successfully!")
                    download_button(output_path, out_name)
                except Exception as e:
                    st.error(f"Error: {e}")

# ══════════════════════════════
# TAB 3 — P2P Success Rate
# ══════════════════════════════
with tab3:
    st.subheader("IPS-P2P Success Rate Report")
    report_date_p2p = st.date_input("Report date", value=date.today(), key="p2p_date")
    col1, col2 = st.columns(2)
    with col1:
        error_file = st.file_uploader("Decline/Error file (.xlsx)", type=["xlsx"], key="p2p_error")
    with col2:
        success_file_p2p = st.file_uploader("IPS Success file (.xlsx)", type=["xlsx"], key="p2p_success")

    if st.button("Generate P2P Report", use_container_width=True, key="btn_p2p"):
        if not error_file or not success_file_p2p:
            st.error("Please upload both files.")
        else:
            with st.spinner("Generating report..."):
                try:
                    error_path = save_upload(error_file)
                    success_path = save_upload(success_file_p2p)
                    out_name = f"IPS-P2P_Success_Rate_Report_for_{report_date_p2p.strftime('%B_%d_%Y')}.xlsx"
                    output_path = os.path.join(tempfile.gettempdir(), out_name)
                    from datetime import datetime
                    generate_p2p_report(error_path, success_path, output_path, datetime.combine(report_date_p2p, datetime.min.time()))
                    st.success("✅ Report generated successfully!")
                    download_button(output_path, out_name)
                except Exception as e:
                    st.error(f"Error: {e}")

# ══════════════════════════════
# TAB 4 — POS Report
# ══════════════════════════════
with tab4:
    st.subheader("POS Successful With Value Report")
    report_date_pos = st.date_input("Report date", value=date.today(), key="pos_date")
    col3, col4 = st.columns(2)
    with col3:
        issuer_file = st.file_uploader("Issuer file (.xlsx)", type=["xlsx"], key="pos_issuer")
    with col4:
        acquirer_file = st.file_uploader("Acquirer file (.xlsx)", type=["xlsx"], key="pos_acquirer")

    if st.button("Generate POS Report", use_container_width=True, key="btn_pos"):
        if not issuer_file or not acquirer_file:
            st.error("Please upload both Issuer and Acquirer files.")
        else:
            with st.spinner("Generating report..."):
                try:
                    issuer_path = save_upload(issuer_file)
                    acquirer_path = save_upload(acquirer_file)
                    out_name = f"POS_Successful_With_Value_{report_date_pos.strftime('%B_%d_%Y')}.xlsx"
                    output_path = os.path.join(tempfile.gettempdir(), out_name)
                    from datetime import datetime
                    generate_pos_report(issuer_path, acquirer_path, output_path, datetime.combine(report_date_pos, datetime.min.time()))
                    st.success("✅ Report generated successfully!")
                    download_button(output_path, out_name)
                except Exception as e:
                    st.error(f"Error: {e}")

# ══════════════════════════════
# TAB 5 — POS Success Rate
# ══════════════════════════════
with tab5:
    st.subheader("POS Success Rate Report")
    report_date_posr = st.date_input("Report date", value=date.today(), key="posr_date")
    posr_file = st.file_uploader("Upload SmartVista POS raw transaction export (.xlsx)", type=["xlsx"], key="posr_file")

    if st.button("Generate POS Success Rate Report", use_container_width=True, key="btn_posr"):
        if not posr_file:
            st.error("Please upload the raw POS transaction export.")
        else:
            with st.spinner("Generating report..."):
                try:
                    input_path = save_upload(posr_file)
                    out_name = f"POS_SUCCESS_RATE_{report_date_posr.strftime('%B_%d_%Y')}.xlsx"
                    output_path = os.path.join(tempfile.gettempdir(), out_name)
                    from datetime import datetime
                    unknown_codes, unmapped_issuers = generate_pos_success_rate_report(
                        input_path, output_path, datetime.combine(report_date_posr, datetime.min.time())
                    )
                    st.success("✅ Report generated successfully!")
                    if unknown_codes:
                        st.warning(f"New response code(s) found and added as extra rows: {unknown_codes}. "
                                   f"Add a remark for them in generate_pos_success_rate_report.py if they recur.")
                    if unmapped_issuers:
                        st.warning(f"New bank(s) found and added as new columns: {unmapped_issuers}.")
                    download_button(output_path, out_name)
                except Exception as e:
                    st.error(f"Error: {e}")

st.markdown("---")
st.caption("EthSwitch S.C. — Internal Report Generator | Built with Streamlit")
