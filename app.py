import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Predictive Maintenance Dashboard",
    layout="wide"
)

st.title("Predictive Maintenance Dashboard")
st.write(
    "Integrated anomaly detection, failure classification, "
    "and Remaining Useful Life (RUL) prediction."
)

# --------------------------------------------------
# LOAD DATA (ONCE)
# --------------------------------------------------
@st.cache_data
def load_data():
    anomaly_df = pd.read_csv("results/anomaly_scores.csv")
    pred_df = pd.read_csv("results/results_df.csv")
    return anomaly_df, pred_df


anomaly_df, pred_df = load_data()

# --------------------------------------------------
# ENGINE SELECTOR (FIXED)
# --------------------------------------------------
# UNION of engines from both projects
engine_ids = sorted(
    set(anomaly_df["engine_id"]) |
    set(pred_df["engine_id"])
)

selected_engine = st.sidebar.selectbox(
    "Select Engine ID",
    engine_ids
)

# --------------------------------------------------
# VIEW SELECTOR
# --------------------------------------------------
mode = st.sidebar.radio(
    "Select View",
    [
        "Anomaly Detection",
        "Failure Prediction & RUL",
        "Combined Health View"
    ]
)

# --------------------------------------------------
# VIEW 1 — ANOMALY DETECTION
# --------------------------------------------------
if mode == "Anomaly Detection":
    st.header("Anomaly Detection")

    df = anomaly_df[
        anomaly_df["engine_id"] == selected_engine
    ].sort_values("cycle")

    if df.empty:
        st.warning("No anomaly data available for this engine.")
    else:
        fig, ax = plt.subplots(figsize=(10, 4))

        ax.plot(
            df["cycle"],
            df["anomaly_score"],
            label="Anomaly Score"
        )

        threshold = df["anomaly_score"].quantile(0.05)
        ax.axhline(
            y=threshold,
            color="red",
            linestyle="--",
            label="Anomaly Threshold"
        )

        ax.set_xlabel("Cycle")
        ax.set_ylabel("Anomaly Score")
        ax.legend()

        st.pyplot(fig)

# --------------------------------------------------
# VIEW 2 — FAILURE PREDICTION & RUL
# --------------------------------------------------
elif mode == "Failure Prediction & RUL":
    st.header("Failure Prediction & RUL")

    df = pred_df[
        pred_df["engine_id"] == selected_engine
    ].sort_values("cycle")

    if df.empty:
        st.warning("No prediction data available for this engine.")
    else:
        fig, ax = plt.subplots(figsize=(10, 4))

        ax.plot(
            df["cycle"],
            df["predicted_RUL"],
            label="Predicted RUL",
            color="blue"
        )

        ax.plot(
            df["cycle"],
            df["true_RUL"],
            label="True RUL",
            color="green",
            alpha=0.6
        )

        ax.set_xlabel("Cycle")
        ax.set_ylabel("RUL")
        ax.legend()

        st.pyplot(fig)

        latest = df.iloc[-1]

        st.subheader("Current Status")
        st.metric("Predicted RUL", f"{int(latest['predicted_RUL'])} cycles")
        st.metric("Failure Probability", f"{latest['fail_probability']:.2f}")

# --------------------------------------------------
# VIEW 3 — COMBINED HEALTH VIEW
# --------------------------------------------------
elif mode == "Combined Health View":
    st.header("Combined Engine Health View")

    df_anom = anomaly_df[
        anomaly_df["engine_id"] == selected_engine
    ].sort_values("cycle")

    df_pred = pred_df[
        pred_df["engine_id"] == selected_engine
    ].sort_values("cycle")

    if df_anom.empty and df_pred.empty:
        st.warning("No data available for this engine.")
    else:
        fig, ax1 = plt.subplots(figsize=(10, 4))

        if not df_pred.empty:
            ax1.plot(
                df_pred["cycle"],
                df_pred["predicted_RUL"],
                color="blue",
                label="Predicted RUL"
            )
            ax1.set_ylabel("RUL", color="blue")
            ax1.tick_params(axis="y", labelcolor="blue")

        ax2 = ax1.twinx()

        if not df_anom.empty:
            ax2.plot(
                df_anom["cycle"],
                df_anom["anomaly_score"],
                color="red",
                alpha=0.6,
                label="Anomaly Score"
            )
            ax2.set_ylabel("Anomaly Score", color="red")
            ax2.tick_params(axis="y", labelcolor="red")

        ax1.set_xlabel("Cycle")
        fig.tight_layout()

        st.pyplot(fig)

        # STATUS LOGIC
        if not df_pred.empty:
            latest_pred = df_pred.iloc[-1]
            latest_anom = (
                df_anom.iloc[-1]
                if not df_anom.empty else None
            )

            st.subheader("Overall Status")

            if latest_pred["fail_probability"] > 0.7:
                st.error("CRITICAL: High failure risk detected")
            elif latest_anom is not None and latest_anom["anomaly_score"] < df_anom["anomaly_score"].quantile(0.05):
                st.warning("Abnormal behavior detected")
            else:
                st.success("Engine operating normally")
