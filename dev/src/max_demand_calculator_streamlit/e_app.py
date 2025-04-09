import streamlit as st

# 🔐 User credentials (email + password)
ALLOWED_USERS = {
    "yathuyoshi@energunite.com": "Energunite.2025",
    "hakan@energunite.com": "StreamLitENRG2025"
}

# Simple login screen
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔐 Login Required")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email in ALLOWED_USERS and password == ALLOWED_USERS[email]:
            st.session_state["authenticated"] = True
            st.experimental_rerun()
        else:
            st.error("Invalid email or password.")
    st.stop()

import streamlit as st
import os
import pandas as pd
from a_loader import load_csv
from b_transformer import transform_dataframe
from c_season import apply_season
from d_calculator import calculate_rolling_max, summarize_top_days, seasonal_summary

st.set_page_config(page_title="Single Meter Max Demand Calculator", layout="wide")
st.image("src/max_demand_calculator/assets/ener_logo.png", width=300)
st.title("Single Meter Max Demand Calculator")
st.markdown("Upload a CSV file for a single meter to analyse the top 5 days and seasonal max 1-hour electricity demand.")

season_styles = {
    "Spring": {"color": "#28a745", "icon": "🌱", "bg": "#e6f4ea"},
    "Summer": {"color": "#ffc107", "icon": "☀️", "bg": "#fff9e6"},
    "Autumn": {"color": "#a0522d", "icon": "🍂", "bg": "#f8efe6"},
    "Winter": {"color": "#007bff", "icon": "❄️", "bg": "#e6f0fa"},
}

uploaded_file = st.file_uploader("📂 Upload your meter CSV", type=["csv"])
output_path = st.text_input("💾 Enter output folder path (optional)", value="")

if uploaded_file:
    df = load_csv(uploaded_file)
    if df is not None:
        df = transform_dataframe(df)
        if df is not None:
            df = apply_season(df)
            df = calculate_rolling_max(df)

            top_days = summarize_top_days(df)
            season_max = seasonal_summary(df)

            tab1, tab2, tab3, tab4 = st.tabs(["🔝 Top 5 Summary", "📋 Detailed Top 5 Table", "📆 Seasonal Summary", "📋 Seasonal Detail Table"])

            with tab1:
                st.subheader("🔝 Top 5 Days with Highest 1-Hour Demand")
                top_day_display = top_days[['MPAN', 'Date', 'Season', 'Rank', 'Total Demand (1-hr) in kW']].copy()
                top_day_display.set_index('Rank', inplace=True)
                st.dataframe(top_day_display.style.background_gradient(
                    subset=["Total Demand (1-hr) in kW"],
                    cmap="YlOrRd",
                    axis=0
                ).set_properties(**{"text-align": "center"}))

                st.download_button("⬇️ Download Top 5 Summary CSV", top_day_display.reset_index().to_csv(index=False),
                                   file_name="top_5_summary.csv", mime="text/csv")

            with tab2:
                st.subheader("📋 Detailed Table – Top 5 Days")
                st.dataframe(top_days.style.set_properties(**{
                    "text-align": "center"
                }).set_table_styles([
                    {"selector": "th", "props": [("text-align", "center")]}
                ]), use_container_width=True)

                st.download_button("⬇️ Download Detailed Top 5 CSV", top_days.to_csv(index=False),
                                   file_name="top_5_detailed.csv", mime="text/csv")

            with tab3:
                st.subheader("📆 Max 1-Hour Demand by Season")
                for _, row in season_max.iterrows():
                    season = row['Season']
                    demand = row['Total Demand (1-hr) in kW']
                    style = season_styles.get(season, {})
                    color = style.get("color", "black")
                    icon = style.get("icon", "")
                    bg = style.get("bg", "#f0f0f0")
                    mpan = row["MPAN"]
                    date = row["Date"]

                    st.markdown(
                        f"""
                        <div style='background-color:{bg}; border-left: 6px solid {color}; padding: 10px; margin: 10px 0; border-radius: 5px;'>
                            <p style='color:{color}; font-size:18px; text-align:center;'>
                            {icon} <strong>{season}</strong> — <span style='color:black'>{demand:.2f} kW</span><br>
                            <small style='color:gray'>MPAN: {mpan} • Date: {date}</small>
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            with tab4:
                st.markdown("### 📋 Detailed Table – Seasonal Peaks")
                st.dataframe(season_max.style.set_properties(**{
                    "text-align": "center"
                }).set_table_styles([
                    {"selector": "th", "props": [("text-align", "center")]}
                ]), use_container_width=True)

                st.download_button("⬇️ Download Detailed Seasonal Summary CSV", season_max.to_csv(index=False),
                                   file_name="seasonal_summary_detailed.csv", mime="text/csv")

            if output_path:
                try:
                    top_days.to_csv(os.path.join(output_path, "top_days.csv"), index=False)
                    season_max.to_csv(os.path.join(output_path, "seasonal_summary.csv"), index=False)
                    st.success("✅ Output files saved successfully!")
                except Exception as e:
                    st.error(f"❌ Error saving files: {e}")

st.markdown("---")
st.info("🔚 To close the app, press Ctrl+C in your terminal or close this browser tab.")