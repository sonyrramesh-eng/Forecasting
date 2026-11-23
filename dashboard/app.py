
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Karnataka Dengue Dashboard",
    page_icon="🦟",
    layout="wide"
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"

# Load datasets
@st.cache_data
def load_data():
    dengue = pd.read_csv(
        OUTPUT_DIR / "karnataka_monthly_dengue_trend.csv"
    )
    rainfall = pd.read_csv(
        OUTPUT_DIR / "karnataka_monthly_rainfall.csv"
    )
    combined = pd.read_csv(
        OUTPUT_DIR / "karnataka_dengue_rainfall_combined.csv"
    )
    predictions = pd.read_csv(
        OUTPUT_DIR / "forecasting_model_predictions.csv"
    )
    performance = pd.read_csv(
        OUTPUT_DIR / "forecasting_model_performance.csv"
    )

    dengue["month"] = pd.to_datetime(dengue["month"])
    rainfall["month"] = pd.to_datetime(rainfall["month"])
    predictions["month"] = pd.to_datetime(predictions["month"])

    return dengue, rainfall, combined, predictions, performance


try:
    dengue, rainfall, combined, predictions, performance = load_data()

except Exception as e:
    st.error(f"Unable to load project datasets: {e}")
    st.stop()


# Dashboard title
st.title("🦟 Karnataka Dengue Trend & Forecasting Dashboard")

st.write(
    "An interactive analysis of historical dengue cases, "
    "rainfall patterns and exploratory forecasting results."
)

st.caption(
    "Study region: Karnataka | "
    "District-level analysis: 31 districts"
)

# Sidebar
st.sidebar.header("Dashboard Navigation")

section = st.sidebar.radio(
    "Select Analysis",
    [
        "Overview",
        "Dengue Analysis",
        "Rainfall Analysis",
        "District Analysis",
        "Forecasting Results"
    ]
)


# OVERVIEW
if section == "Overview":

    st.header("Project Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Dengue Cases",
        f"{int(dengue['total_dengue_cases'].sum()):,}"
    )

    col2.metric(
        "Districts Covered",
        "31"
    )

    col3.metric(
        "Monthly Records",
        len(dengue)
    )

    st.subheader("Monthly Dengue Trend")

    fig = px.line(
        dengue,
        x="month",
        y="total_dengue_cases",
        markers=True,
        title="Monthly Dengue Cases in Karnataka"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Yearly Dengue Summary")

    yearly = dengue.copy()
    yearly["year"] = yearly["month"].dt.year

    yearly_summary = yearly.groupby("year", as_index=False)[
        "total_dengue_cases"
    ].sum()

    fig = px.bar(
        yearly_summary,
        x="year",
        y="total_dengue_cases",
        title="Yearly Dengue Cases"
    )

    st.plotly_chart(fig, use_container_width=True)


# DENGUE ANALYSIS
elif section == "Dengue Analysis":

    st.header("Dengue Analysis")

    fig = px.line(
        dengue,
        x="month",
        y=["total_dengue_cases", "total_suspected"],
        markers=True,
        title="Monthly Confirmed and Suspected Cases"
    )

    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(
        dengue,
        x="month",
        y="total_deaths",
        title="Monthly Dengue Deaths"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Monthly Dengue Data")
    st.dataframe(dengue, use_container_width=True)


# RAINFALL ANALYSIS
elif section == "Rainfall Analysis":

    st.header("Rainfall Analysis")

    fig = px.line(
        rainfall,
        x="month",
        y="average_district_rainfall_mm",
        markers=True,
        title="Monthly Average District Rainfall"
    )

    st.plotly_chart(fig, use_container_width=True)

    comparison = dengue.merge(
        rainfall,
        on="month",
        how="inner"
    )

    fig = px.scatter(
        comparison,
        x="average_district_rainfall_mm",
        y="total_dengue_cases",
        hover_data=["month"],
        title="Rainfall vs Dengue Cases"
    )

    st.plotly_chart(fig, use_container_width=True)


# DISTRICT ANALYSIS
elif section == "District Analysis":

    st.header("District-wise Dengue Analysis")

    district = st.selectbox(
        "Select District",
        sorted(combined["district"].dropna().unique())
    )

    district_data = combined[
        combined["district"] == district
    ].copy()

    district_data["date"] = pd.to_datetime(
        district_data["date"]
    )

    monthly = district_data.set_index("date").resample("MS").agg(
        dengue_cases=("daily_cases", "sum"),
        rainfall_mm=("average_rainfall_mm", "mean")
    ).reset_index()

    fig = px.line(
        monthly,
        x="date",
        y="dengue_cases",
        markers=True,
        title=f"Monthly Dengue Cases - {district}"
    )

    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(
        monthly,
        x="date",
        y="rainfall_mm",
        markers=True,
        title=f"Monthly Average Rainfall - {district}"
    )

    st.plotly_chart(fig, use_container_width=True)


# FORECASTING RESULTS
elif section == "Forecasting Results":

    st.header("Forecasting Model Results")

    st.subheader("Model Performance")

    st.dataframe(
        performance,
        use_container_width=True,
        hide_index=True
    )

    fig = px.bar(
        performance,
        x="Model",
        y="MAE",
        title="Model Comparison - MAE"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Actual vs Predicted Cases")

    fig = px.line(
        predictions,
        x="month",
        y=[
            "actual_cases",
            "baseline_prediction",
            "model_a_prediction",
            "model_b_prediction"
        ],
        markers=True,
        title="Actual vs Predicted Dengue Cases"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "The baseline performed best in this initial experiment. "
        "Forecasting results are exploratory because the test set "
        "contains only seven monthly observations."
    )


st.sidebar.markdown("---")
st.sidebar.caption("Karnataka Dengue Trend & Forecasting Project")
