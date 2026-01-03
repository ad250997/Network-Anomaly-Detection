import streamlit as st
import requests
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
API_URL = "http://localhost:5000/predict"

st.set_page_config(
    page_title="Network Anomaly Detection",
    layout="wide"
)

# -----------------------------
# SERVICE GROUP → CANONICAL SERVICE
# -----------------------------
SERVICE_GROUP_MAP = {
    "HTTP-related": "http",
    "File Transfer": "ftp_data",
    "Remote Access": "telnet",
    "Email": "smtp",
    "DNS": "domain_u",
    "Other": "other"
}

FLAG_MAP = {
    "Normal": "SF",
    "Error": "REJ",
    "Suspicious": "S0"
}

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("Input Mode")
mode = st.sidebar.radio(
    "Select mode",
    ["Single Connection", "Batch (CSV Upload)"]
)

# -----------------------------
# MAIN TITLE
# -----------------------------
st.title("Network Anomaly Detection System")
st.write(
    "This application demonstrates anomaly detection on network connections "
    "using a trained ML model based on the NSL-KDD dataset."
)

# =========================================================
# MODE 1: SINGLE CONNECTION
# =========================================================
if mode == "Single Connection":

    st.subheader("Manual Connection Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        protocol_type = st.selectbox(
            "Protocol",
            ["tcp", "udp", "icmp"]
        )

        service_group = st.selectbox(
            "Service Group",
            list(SERVICE_GROUP_MAP.keys())
        )

        flag_group = st.selectbox(
            "Connection Flag",
            list(FLAG_MAP.keys())
        )

    with col2:
        srcbytes = st.number_input(
            "Source Bytes",
            min_value=0,
            value=200
        )

        dstbytes = st.number_input(
            "Destination Bytes",
            min_value=0,
            value=3000
        )

        loggedin = st.selectbox(
            "Logged In",
            [0, 1]
        )

    with col3:
        count = st.slider(
            "Connections to Same Host",
            min_value=0,
            max_value=500,
            value=10
        )

        srvcount = st.slider(
            "Connections to Same Service",
            min_value=0,
            max_value=500,
            value=10
        )

    if st.button("Predict"):

        payload = {
            "protocoltype": protocol_type,
            "service": SERVICE_GROUP_MAP[service_group],
            "flag": FLAG_MAP[flag_group],
            "srcbytes": srcbytes,
            "dstbytes": dstbytes,
            "loggedin": loggedin,
            "count": count,
            "srvcount": srvcount
        }

        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        result = response.json()

        st.markdown("### Prediction Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Prediction",
                result.get("prediction", "N/A")
            )

        with col2:
            if "probability" in result:
                st.metric(
                    "Confidence",
                    f"{result['probability']:.2%}"
                )

        if "attack_type" in result:
            st.write(f"**Attack Type:** {result['attack_type']}")

        if "explanation" in result:
            st.markdown("### Explanation")
            st.write(result["explanation"])

# =========================================================
# MODE 2: BATCH CSV
# =========================================================
else:

    st.subheader("Batch Connection Analysis")

    uploaded_file = st.file_uploader(
        "Upload CSV file",
        type=["csv"]
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded data:")
        st.dataframe(df.head())

        if st.button("Run Batch Prediction"):

            try:
                response = requests.post(
                    API_URL,
                    json={"batch": df.to_dict(orient="records")}
                )
                response.raise_for_status()
                result = response.json()

                preds = pd.DataFrame(result["predictions"])

                st.markdown("### Batch Summary")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Total Connections",
                        len(preds)
                    )

                with col2:
                    anomaly_rate = (
                        (preds["prediction"] != "normal").mean() * 100
                    )
                    st.metric(
                        "Anomalous Connections (%)",
                        f"{anomaly_rate:.2f}"
                    )

                st.markdown("### Sample Predictions")
                st.dataframe(preds.head(20))

            except requests.exceptions.RequestException:
                st.error("API error during batch prediction.")

