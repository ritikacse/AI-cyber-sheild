
import streamlit as st
import pandas as pd
from pathlib import Path

from detectors.url_detector import URLDetector
from detectors.text_detector import TextDetector


# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(
    page_title="AI Cyber Shield",
    page_icon="🛡️",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent


# =========================
# CUSTOM DESIGN
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #06111f, #102b46, #02060c);
    color: #eaf6ff;
}
h1, h2, h3 {
    color: #00d9ff !important;
}
[data-testid="stMetric"] {
    background: rgba(0, 217, 255, 0.08);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(0, 217, 255, 0.25);
}
div.stButton > button {
    background-color: #007ca8;
    color: white;
    border: 1px solid #00d9ff;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# INITIALIZE DETECTORS
# =========================
url_detector = URLDetector()
text_detector = TextDetector()


# =========================
# DATASET LOADER
# =========================
def load_dataset(filename):
    file_path = BASE_DIR / filename

    if not file_path.exists():
        return None

    try:
        return pd.read_csv(file_path)
    except (OSError, pd.errors.ParserError, UnicodeDecodeError):
        return None


# =========================
# HEADER
# =========================
st.title("🛡️ AI CYBER SHIELD")
st.markdown(
    "### Intelligent Cybersecurity Monitoring Dashboard"
)
st.caption(
    "Educational URL screening, suspicious email analysis, "
    "and network dataset exploration."
)

# =========================
# DASHBOARD METRICS
# =========================
url_df = load_dataset("url_dataset.csv")
email_df = load_dataset("email_dataset.csv")
network_df = load_dataset("network_dataset.csv")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "URL Records",
        len(url_df) if url_df is not None else 0
    )

with c2:
    st.metric(
        "Email Records",
        len(email_df) if email_df is not None else 0
    )

with c3:
    st.metric(
        "Network Records",
        len(network_df) if network_df is not None else 0
    )


# =========================
# APPLICATION TABS
# =========================
url_tab, email_tab, network_tab, data_tab, about_tab = st.tabs([
    "🔗 URL Scanner",
    "📧 Email Scanner",
    "🌐 Network Data",
    "📊 Datasets",
    "ℹ️ About"
])


# =========================
# URL SCANNER
# =========================
with url_tab:
    st.subheader("Check a suspicious URL")

    url = st.text_input(
        "Enter URL",
        placeholder="https://example.com"
    )

    if st.button("Analyze URL", key="url_scan"):
        if not url.strip():
            st.warning("Please enter a URL.")
        else:
            try:
                result = url_detector.predict(url)

                st.write("**Assessment:**", result.get(
                    "risk", result.get("status", "Unknown")
                ))

                for reason in result.get("reasons", []):
                    st.write(f"- {reason}")

            except Exception as error:
                st.error(f"URL detector error: {error}")

    st.info(
        "This scanner uses the rules implemented in your detector. "
        "A clean result does not guarantee that a URL is safe."
    )


# =========================
# EMAIL SCANNER
# =========================
with email_tab:
    st.subheader("Analyze an email or message")

    email_text = st.text_area(
        "Paste email content",
        placeholder="Paste a suspicious email here..."
    )

    if st.button("Analyze Email", key="email_scan"):
        if not email_text.strip():
            st.warning("Please enter email text.")
        else:
            try:
                result = text_detector.predict(email_text)

                st.write("**Assessment:**", result.get(
                    "risk", result.get("status", "Unknown")
                ))

                for reason in result.get("reasons", []):
                    st.write(f"- {reason}")

            except Exception as error:
                st.error(f"Text detector error: {error}")


# =========================
# NETWORK DATA
# =========================
with network_tab:
    st.subheader("Network Dataset")

    if network_df is not None:
        st.dataframe(network_df, use_container_width=True)

        if "label" in network_df.columns:
            st.subheader("Record labels")
            st.bar_chart(network_df["label"].value_counts())
    else:
        st.warning(
            "network_dataset.csv was not found in the repository root."
        )


# =========================
# ALL DATASETS
# =========================
with data_tab:
    st.subheader("Explore Project Datasets")

    datasets = {
        "URL Dataset": url_df,
        "Email Dataset": email_df,
        "Network Dataset": network_df
    }

    for title, dataframe in datasets.items():
        with st.expander(title):
            if dataframe is not None:
                st.write(f"Total records: {len(dataframe)}")
                st.dataframe(dataframe, use_container_width=True)

                st.download_button(
                    label=f"Download {title}",
                    data=dataframe.to_csv(index=False),
                    file_name=title.lower().replace(" ", "_") + ".csv",
                    mime="text/csv",
                    key=title
                )
            else:
                st.warning("Dataset file not found.")


# =========================
# ABOUT
# =========================
with about_tab:
    st.subheader("About AI Cyber Shield")

    st.write("""
    AI Cyber Shield is an educational cybersecurity project.

    Features:
    - URL risk screening
    - Suspicious email and message analysis
    - Network dataset visualization
    - Dataset exploration and downloads

    The detection results depend on the rules implemented in the
    detector modules. This version does not independently monitor
    live network traffic or guarantee accurate threat detection.
    """)

    st.markdown(
        "[Cybersecurity awareness resources](https://www.cisa.gov/secure-our-world)"
    )


# =========================
# FOOTER
# =========================
st.divider()
st.caption("AI Cyber Shield | Python + Streamlit")
