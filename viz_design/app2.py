# aktuellste version 03.05-26 bessseres als travel_dashboard
import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path
from datetime import date

st.set_page_config(
    page_title="Travel Insights Dashboard",
    page_icon="✈️",
    layout="wide",
)

DATA_FILE = Path(__file__).parent.parent / "data_acquisition" / "traveldata-export.xlsx"

# =========================
# STYLING
# =========================
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1450px;
        padding-top: 0.8rem !important;
        margin-top: -12px !important;
        padding-bottom: 2rem;
    }

    header { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }

    .stApp {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        color: white;
    }

    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: white !important;
    }

    [data-testid="stSelectbox"] label {
        color: white !important;
        font-weight: 600;
        font-size: 0.92rem !important;
    }

    [data-testid="stSelectbox"] > div > div,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: white !important;
        border-radius: 8px !important;
        min-height: 40px !important;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] *,
    [data-testid="stSelectbox"] div[data-baseweb="select"] span,
    [data-testid="stSelectbox"] div[data-baseweb="select"] div,
    [data-testid="stSelectbox"] div[data-baseweb="select"] input,
    [data-testid="stSelectbox"] div[data-baseweb="select"] p,
    [data-testid="stSelectbox"] [class*="singleValue"],
    [data-testid="stSelectbox"] [class*="SingleValue"],
    [data-testid="stSelectbox"] [class*="valueContainer"],
    [data-testid="stSelectbox"] [class*="ValueContainer"],
    [data-testid="stSelectbox"] div[role="button"],
    [data-testid="stSelectbox"] div[role="button"] * {
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        fill: #111827 !important;
    }

    [data-testid="stSelectbox"] svg {
        fill: #111827 !important;
        color: #111827 !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="popover"] * {
        color: #111827 !important;
    }

    ul[role="listbox"] {
        background-color: white !important;
    }

    ul[role="listbox"] li {
        color: #111827 !important;
        background-color: white !important;
    }

    ul[role="listbox"] li:hover {
        background-color: #f3f4f6 !important;
    }

    div[data-testid="stButton"] button {
        background-color: white !important;
        color: #111827 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }

    div[data-testid="stButton"] button * {
        color: #111827 !important;
    }

    .vg-tooltip,
    .vg-tooltip * {
        color: #111827 !important;
        background-color: white !important;
        border-color: rgba(0,0,0,0.15) !important;
    }

    .vg-tooltip table,
    .vg-tooltip tbody,
    .vg-tooltip tr,
    .vg-tooltip td,
    .vg-tooltip th {
        color: #111827 !important;
        background-color: white !important;
    }

    [data-testid="stElementToolbar"] {
        background: transparent !important;
    }

    [data-testid="stElementToolbar"] button {
        background: rgba(255,255,255,0.92) !important;
        border: 1px solid rgba(0,0,0,0.15) !important;
        border-radius: 6px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.18) !important;
        padding: 1px !important;        /* ← slimmer frame around icon */
        width: 24px !important;         /* ← tighter button size */
        height: 24px !important;
    }

    [data-testid="stElementToolbar"] svg {
        width: 18px !important;
        height: 18px !important;
        color: #111827 !important;
    }

    [data-testid="stElementToolbar"] svg path,
    [data-testid="stElementToolbar"] svg polyline,
    [data-testid="stElementToolbar"] svg line,
    [data-testid="stElementToolbar"] svg rect,
    [data-testid="stElementToolbar"] svg circle {
        stroke: #111827 !important;
        fill: none !important;         /* ← let the icon be an outline, not a blob */
    }

    .vega-actions {
        background: white !important;
        border-radius: 8px !important;
        padding: 6px !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.22) !important;
    }

    .vega-actions,
    .vega-actions *,
    .vega-actions a {
        color: #111827 !important;
        background-color: white !important;
    }


    .section-panel {
        background: rgba(255,255,255,0.018);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px;
        padding: 16px 18px 12px 18px;
        height: 100%;
    }

    .section-title {
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.12);
    }

    .small-filter-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 12px;
        padding: 12px 12px 6px 12px;
        max-width: 330px;
        margin-left: auto;
        margin-top: 6px;
    }

    .small-filter-title {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.85) !important;
        margin-bottom: 4px;
    }

    .budget-card {
        background: rgba(255,255,255,0.018);
        # border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 18px;
    }

    .budget-title {
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 28px;
    }

    .progress-bg {
        width: 100%;
        height: 34px;
        background: rgba(255,255,255,0.18);
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 14px;
        position: relative;
    }

    .progress-fill {
        height: 100%;
        border-radius: 10px;
    }

    .budget-marker {
        position: absolute;
        top: 0;
        bottom: 0;
        width: 3px;
        background-color: #ffffff;
        box-shadow: 0 0 4px rgba(0,0,0,0.5);
        z-index: 10;
    }

    .budget-row {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        font-weight: 700;
    }

    .budget-percent {
        font-size: 28px;
    }

    .budget-detail {
        font-size: 16px;
        opacity: 0.9;
        text-align: right;
    }

    # .cost-box {
    #     background: #49852f;
    #     border-radius: 14px;
    #     padding: 18px 22px;
    #     margin-top: 18px;
    #     margin-bottom: 18px;
    #     box-shadow: 0 4px 18px rgba(0,0,0,0.18);
    # }
    .cost-box {
        background: rgba(255,255,255,0.018);
        border-radius: 14px;
        padding: 16px 18px;
        margin-top: 18px;
        margin-bottom: 18px;
    }

    .cost-label {
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .cost-value {
        font-size: 38px;
        font-weight: 800;
    }

    .date-box {
        font-size: 14px;
        font-weight: 700;
        text-align: right;
        color: rgba(255,255,255,0.9) !important;
        margin-top: 4px;
    }

    .analysis-context {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 16px;
        font-size: 16px;
        font-weight: 700;
    }

    .analysis-metric-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin-bottom: 18px;
    }

    .analysis-metric-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 12px;
        padding: 14px 16px;
    }

    .analysis-metric-label {
        font-size: 14px;
        font-weight: 700;
        opacity: 0.9;
        margin-bottom: 6px;
    }

    .analysis-metric-value {
        font-size: 26px;
        font-weight: 800;
    }

    .budget-history-row {
        display: grid;
        grid-template-columns: 55px 1fr 70px 34px;
        gap: 12px;
        align-items: center;
        margin-bottom: 12px;
        font-weight: 700;
    }

    .budget-history-year {
        font-size: 15px;
    }

   .budget-history-bg {
        height: 18px;
        background: rgba(255,255,255,0.18);
        border-radius: 8px;
        overflow: hidden;
        position: relative;
    }

    .budget-history-fill {
        height: 100%;
        border-radius: 8px;
    }

    .budget-history-percent {
        font-size: 15px;
        text-align: right;
    }

    .budget-status {
        font-size: 18px;
        text-align: center;
    }

    hr {
        border-color: rgba(255,255,255,0.12);
        margin-top: 0.6rem;
        margin-bottom: 0.8rem;
    }

    /* remove ghost boxes from widget wrappers only */
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] > div,
    [data-testid="stElementToolbar"] + div,
    .stSelectbox > div:first-child,
    [data-testid="stMarkdownContainer"] > div:empty,
    [data-testid="element-container"]:empty {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] *,
    ul[role="listbox"],
    ul[role="listbox"] li,
    ul[role="listbox"] li * {
        background-color: #ffffff !important;
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
    }

    ul[role="listbox"] li:hover {
        background-color: #f3f4f6 !important;
    }

    html[data-theme="dark"] div[role="tooltip"],
    html[data-theme="dark"] div[role="tooltip"] *,
    div[data-testid="stDownloadButton"] button {
        background: transparent !important;
        color: rgba(255,255,255,0.5) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 4px !important;
        font-size: 16px !important;
        font-weight: 400 !important;
        padding: 0px 4px !important;
        margin-top: 0px !important;
        margin-bottom: -12px !important;
        min-height: 0 !important;
        height: 24px !important;
        width: 24px !important;
        line-height: 1 !important;
    }

    div[data-testid="stDownloadButton"] button:hover {
        color: rgba(255,255,255,0.95) !important;
        background: rgba(255,255,255,0.08) !important;
    }

    div[data-testid="stDownloadButton"] button p {
        font-size: 16px !important;
        margin: 0 !important;
    }

    div[role="tooltip"],
    div[role="tooltip"] * {
        background-color: #ffffff !important;
        color: #111827 !important;
    }

    [data-testid="element-container"]:has([data-testid="stDataFrame"][aria-label="travel_options_table"]) + div [data-testid="stElementToolbar"] {
        display: none !important;
    }

    [data-testid="stTable"] {
        transform: scale(0.95);
        transform-origin: top left;
        width: 118% !important;
    }

    [data-testid="stTable"] table {
        font-size: 13px !important;
        width: 100% !important;
        border-collapse: collapse !important;
        table-layout: auto !important;
    }

    [data-testid="stTable"] th {
        font-size: 13px !important;
        font-weight: 700 !important;
        padding: 5px 6px !important;
        color: white !important;
        white-space: nowrap !important;
        border-bottom: 1px solid rgba(255,255,255,0.2) !important;
    }

    [data-testid="stTable"] td {
        font-size: 13px !important;
        padding: 5px 6px !important;
        color: white !important;
        background-color: #0f172a !important;
        white-space: nowrap !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# DATA
# =========================
@st.cache_data
def load_data(path: Path):
    df = pd.read_excel(path, sheet_name="travel_data")
    budgets = pd.read_excel(path, sheet_name="co2_budgets")

    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

    df["cost_CHF"] = pd.to_numeric(df["cost_CHF"], errors="coerce")
    df["CO2e RFI2.7 (t)"] = pd.to_numeric(df["CO2e RFI2.7 (t)"], errors="coerce")
    df["km"] = pd.to_numeric(df["km"], errors="coerce")

    df["subunit"] = df["subunit"].astype(str).str.strip()
    budgets["subunit"] = budgets["subunit"].astype(str).str.strip()
    budgets["year"] = pd.to_numeric(budgets["year"], errors="coerce")
    budgets["co2_budget_t"] = pd.to_numeric(budgets["co2_budget_t"], errors="coerce")

    return df, budgets


df, budgets = load_data(DATA_FILE)

# =========================
# HELPERS
# =========================
def format_chf(x):
    return f"{x:,.0f} CHF".replace(",", "’")


def format_tonnes(x):
    if x is None or pd.isna(x):
        return "-"
    return f"{x:,.1f} t".replace(",", "’")


def format_percent(x):
    if x is None or pd.isna(x):
        return "-"
    return f"{x:.0f}%"


def format_int(x):
    return f"{int(round(x)):,}".replace(",", "’")


def panel_start(title):
    st.markdown('<div class="section-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def panel_end():
    st.markdown("</div>", unsafe_allow_html=True)


def get_budget(budgets_df, selected_subunit, selected_year):
    b = budgets_df[budgets_df["year"] == selected_year].copy()

    if selected_subunit != "All":
        b = b[b["subunit"] == selected_subunit]

    valid = b["co2_budget_t"].dropna()
    if valid.empty:
        return None

    return valid.sum()


def get_status(pct):
    if pct is None or pd.isna(pct):
        return "➖", "No budget"
    if pct > 100:
        return "❌", "Over budget"
    if pct >= 80:
        return "⚠️", "Critical"
    return "✅", "Within budget"


def get_bar_color(pct):
    if pct is None or pd.isna(pct):
        return "rgba(255,255,255,0.18)"
    if pct > 100:
        return "linear-gradient(90deg, #dc2626, #991b1b)"
    if pct >= 80:
        return "linear-gradient(90deg, #f7941d, #d97706)"
    return "linear-gradient(90deg, #2e7d32, #1b5e20)"   

# define Chart theme for better visibility
def altair_theme():
    return {
        "config": {
            #"background": "#032d73",
            #"background": "#1e293b3d"
            "background": "#172133",
            "view": {
                "stroke": "transparent",
                "fill": "#172133",
                },
            "axis": {
                "labelColor": "white",
                "titleColor": "white",
                "gridColor": "rgba(255,255,255,0.18)",
                "domainColor": "rgba(255,255,255,0.35)",
                "tickColor": "rgba(255,255,255,0.35)",
            },
            "legend": {
                "labelColor": "white",
                "titleColor": "white",
            },
            "title": {"color": "white",
                      "fontSize": 28,        # <-- adjust title font size
                      "anchor": "start",     # <-- adjust title anchor
                      "offset": 15           # <-- adjust title offset
            },},
        }


alt.themes.register("travel_dark", altair_theme)
alt.themes.enable("travel_dark")

# =========================
# SESSION STATE
# =========================
if "dashboard_view" not in st.session_state:
    st.session_state.dashboard_view = "Overview"

# =========================
# GLOBAL OPTIONS
# =========================
current_year = 2025
max_analysis_year = 2025

year_options = ["All"] + sorted([y for y in df["year"].dropna().unique().tolist() if y <= max_analysis_year], reverse=True)
subunit_options = ["All"] + sorted(df["subunit"].dropna().unique().tolist())
all_departures = ["All"] + sorted(df["departure_iata"].dropna().unique().tolist())
all_arrivals = ["All"] + sorted(df["arrival_iata"].dropna().unique().tolist())
#used_co2 = 0

# =========================
# HEADER
# =========================
header_left, header_right = st.columns([6, 2.2])

with header_left:
    st.markdown(
        f"<h1 style='text-align:left; margin-top:0.4rem; margin-bottom:0;'>Travel Insights Dashboard</h1>"
        f"<div style='font-size: 2rem; font-weight: 600; color: rgba(255,255,255,0.8); margin-top: 2px;'>Year {current_year}</div>",
        unsafe_allow_html=True,
    )

with header_right:
    st.markdown('<div class="small-filter-box" style="margin-bottom: 5px;">', unsafe_allow_html=True)
    
    b1, b2 = st.columns(2)
    with b1:
        if st.button("Overview", use_container_width=True):
            st.session_state.dashboard_view = "Overview"
    with b2:
        if st.button("Analysis", use_container_width=True):
            st.session_state.dashboard_view = "Analysis"

    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown(
        f"<div class='date-box' style='padding-right: 10px;'>TODAY: {date.today().strftime('%d.%m.%Y')}</div>",
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)



# =========================
# Overview DASHBOARD
# =========================
if st.session_state.dashboard_view == "Overview":

    filter_col, spacer = st.columns([1.25, 4.75])

    with filter_col:
        subunit = st.selectbox("Choose Subunit", subunit_options, index=0, key="overview_subunit")

    overview_df = df[df["year"] == current_year].copy()

    if subunit != "All":
        overview_df = overview_df[overview_df["subunit"] == subunit]

    used_co2 = overview_df["CO2e RFI2.7 (t)"].sum()
    travel_cost = overview_df["cost_CHF"].sum()
    total_company_cost = df[df["year"] == current_year]["cost_CHF"].sum()
    subunit_share = (travel_cost / total_company_cost * 100) if total_company_cost > 0 else 0
    budget = get_budget(budgets, subunit, current_year)
    usage_pct = (used_co2 / budget * 100) if budget and budget > 0 else None
    
    # Dynamische Skalierung
    if usage_pct is not None:
        max_scale = max(100.0, usage_pct) # Skala ist mind. 100, oder der tatsächliche Wert
        progress_width = (usage_pct / max_scale) * 100
        marker_pos = (100.0 / max_scale) * 100
    else:
        progress_width = 0
        marker_pos = 100

    left, right = st.columns([1, 1.15], gap="large")

    with left:
        panel_start(f"Subunit Overview {current_year}")

        if budget and budget > 0:
            progress_color = get_bar_color(usage_pct)

            budget_html = f"""
            <div class="budget-card">
                <div class="budget-title" style="margin-bottom: 10px;">CO₂ Budget</div>
                <div style="position:relative; height:18px; margin-bottom:4px;">
                    <div style="position:absolute; left:{marker_pos}%; transform:translateX(-50%); font-size:11px; font-weight:700; color:white; white-space:nowrap; text-shadow:0 1px 3px rgba(0,0,0,0.8);">100%</div>
                </div>
                <div class="progress-bg">
                    <div class="progress-fill" style="width: {progress_width}%; background: {progress_color};"></div>
                    <div class="budget-marker" style="left: {marker_pos}%;" title="100% Budget limit"></div>
                    <div style="position:absolute; left:12px; top:50%; transform:translateY(-50%); font-size:20px; font-weight:800; color:white; text-shadow:0 1px 3px rgba(0,0,0,0.5);">{format_percent(usage_pct)}</div>
                </div>
            </div>
            """

            st.markdown(budget_html, unsafe_allow_html=True)

        else:
            st.warning("For this subunit, no CO₂ budget was found for the year 2025.")

        if subunit != "All":
            cost_context = f"{subunit_share:.1f}% of total company travel costs"
        else:
            cost_context = "Total company travel costs"

        st.markdown(
            f"""
            <div class="cost-box">
                <div class="cost-label">Travel Costs</div>
                <div style="display:flex; align-items:baseline; gap:18px;">
                    <div class="cost-value">{format_chf(travel_cost)}</div>
                    <div style="font-size:18px; font-weight:600; opacity:0.75; padding-left:24px;">
                        {cost_context}
                    </div>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    with right:
        panel_start("Travel Options")

        route_col1, route_col2 = st.columns(2)

        with route_col1:
            departure = st.selectbox("Departure Location", all_departures, index=0)

        with route_col2:
            arrival = st.selectbox("Arrival Location", all_arrivals, index=0)

        route_df = df.copy()

        if departure != "All":
            route_df = route_df[route_df["departure_iata"] == departure]

        if arrival != "All":
            route_df = route_df[route_df["arrival_iata"] == arrival]

        st.markdown(
            f"""
            <div style="margin:10px 0 12px 0; font-weight:600;">
                Data Basis: <span style="color:#dfe9ff;">all years</span><br>
                Route: <span style="color:#dfe9ff;">{departure if departure != "All" else "all departure locations"} → {arrival if arrival != "All" else "all destination locations"}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if departure == "All" or arrival == "All":
            st.info("Please select a departure and destination location.")
        elif route_df.empty:
            st.warning("No data available for this route.")
        else:
            summary = (
                route_df.groupby("transport_mode", as_index=False)
                .agg(
                    trips=("transport_mode", "size"),
                    avg_cost=("cost_CHF", "mean"),
                    avg_co2_t=("CO2e RFI2.7 (t)", "mean"),
                    avg_km=("km", "mean"),
                )
            )

            mode_order = ["flight", "train", "bus", "rental_car"]
            summary["sort"] = summary["transport_mode"].apply(
                lambda x: mode_order.index(x) if x in mode_order else 99
            )
            summary = summary.sort_values("sort").drop(columns="sort")

            summary["Option"] = summary["transport_mode"].replace(
                {
                    "flight": "Flight",
                    "train": "Train",
                    "bus": "Bus",
                    "rental_car": "Rental Car",
                }
            )

            summary["Ø cost"] = summary["avg_cost"].map(lambda x: format_chf(x) if pd.notna(x) else "-")
            summary["Ø CO₂"] = summary["avg_co2_t"].map(lambda x: f"{x*1000:.0f} kg" if pd.notna(x) else "-")
            summary["Ø distance"] = summary["avg_km"].map(lambda x: f"{x:,.0f} km".replace(",", "’") if pd.notna(x) else "-")

            min_cost = summary["avg_cost"].min()
            min_co2 = summary["avg_co2_t"].min()

            def recommendation(row):
                tags = []
                if row["avg_cost"] == min_cost:
                    tags.append("cheapest")
                if row["avg_co2_t"] == min_co2:
                    tags.append("most environmentally friendly")
                if not tags:
                    return "—"
                return ("Cheapest & most environmentally friendly option"
                        if len(tags) == 2
                        else tags[0].capitalize() + " option")

            summary["recommendation"] = summary.apply(recommendation, axis=1)

            show_df = summary[
                ["Option", "trips", "Ø distance", "Ø cost", "Ø CO₂", "recommendation"]
            ].rename(columns={"trips": "Number of Trips"})

            st.table(show_df)

        panel_end()

# =========================
# ANALYSE DASHBOARD
# =========================
else:
    filter_col1, filter_col2, spacer = st.columns([1.2, 1.4, 3.4])

    with filter_col1:
        analysis_year = st.selectbox("Choose Year", year_options, index=0, key="analysis_year")

    with filter_col2:
        analysis_subunit = st.selectbox("Choose Subunit", subunit_options, index=0, key="analysis_subunit")

    analysis_df = df[df["year"] <= max_analysis_year].copy()

    if analysis_year != "All":
        analysis_df = analysis_df[analysis_df["year"] == analysis_year]

    if analysis_subunit != "All":
        analysis_df = analysis_df[analysis_df["subunit"] == analysis_subunit]

    left, right = st.columns([1.15, 1], gap="large")

    with left:
        st.markdown('<div class="section-panel">', unsafe_allow_html=True)

        if analysis_year == "All":
            line_year = current_year
        else:
            line_year = int(analysis_year)

        # ── Block 1: cumulative current year ──────────────────────────────
        line_df = df[(df["year"] == line_year) & (df["year"] <= max_analysis_year)].copy()

        if analysis_subunit != "All":
            line_df = line_df[line_df["subunit"] == analysis_subunit]

        line_df = (
            line_df.groupby("month", as_index=False)
            .agg(monthly_co2=("CO2e RFI2.7 (t)", "sum"))
            .sort_values("month")
        )

        if line_df.empty:
            st.info("No data available for the yearly trend.")
        else:
            all_months = pd.DataFrame(
                {"month": pd.date_range(start=f"{line_year}-01-01", end=f"{line_year}-12-01", freq="MS")}
            )
            line_df = all_months.merge(line_df, on="month", how="left")
            line_df["monthly_co2"] = line_df["monthly_co2"].fillna(0)
            line_df["cumulative_co2"] = line_df["monthly_co2"].cumsum()

            line_budget = get_budget(budgets, analysis_subunit, line_year)

            co2_line = (
                alt.Chart(line_df)
                .mark_line(point=alt.OverlayMarkDef(color="white", size=30, filled=True), strokeWidth=2, color="#ffa73a")
                .encode(
                    x=alt.X("month:T", title="Month", axis=alt.Axis(format="%b", labelAngle=0)),
                    y=alt.Y("cumulative_co2:Q", title="Cumulative CO₂ Emissions (t)"),
                    tooltip=[
                        alt.Tooltip("month:T", title="Month", format="%b %Y"),
                        alt.Tooltip("monthly_co2:Q", title="CO₂ in Month (t)", format=",.1f"),
                        alt.Tooltip("cumulative_co2:Q", title="CO₂ Cumulative (t)", format=",.1f"),
                    ],
                )
            )

            if line_budget and line_budget > 0:
                budget_rule_data = pd.DataFrame({"budget": [line_budget]})
                budget_rule = (
                    alt.Chart(budget_rule_data)
                    .mark_rule(color="#dc2626", strokeWidth=3, strokeDash=[6, 4])
                    .encode(y="budget:Q", tooltip=[alt.Tooltip("budget:Q", title="Budget limit (t)", format=",.1f")])
                )
                budget_label = (
                    alt.Chart(budget_rule_data)
                    .mark_text(align="left", baseline="bottom", dy=-6, color="#dc2626", fontWeight=600, fontSize=13)
                    .encode(y="budget:Q", x=alt.value(10), text=alt.value(f'Budget limit {line_budget:,.1f} t'))
                )
                line_chart = (co2_line + budget_rule + budget_label).properties(title=f"Cumulative CO₂ Emissions {line_year} – {analysis_subunit}", height=330)
            else:
                line_chart = co2_line.properties(title=f"Cumulative CO₂ Emissions {line_year} – {analysis_subunit}", height=330)

            st.download_button("⬇", data=line_chart.to_html(), file_name="co2_yearly_trend.html", mime="text/html", help="Download chart")
            st.altair_chart(line_chart, use_container_width=True)

        # ── Block 2: CO₂ by transport mode ───────────────────────────────
        mode_df = df[df["year"] <= max_analysis_year].copy()

        if analysis_year != "All":
            mode_df = mode_df[mode_df["year"] == int(analysis_year)]

        if analysis_subunit != "All":
            mode_df = mode_df[mode_df["subunit"] == analysis_subunit]

        mode_co2 = (
            mode_df.groupby("transport_mode", as_index=False)
            .agg(total_co2=("CO2e RFI2.7 (t)", "sum"), trip_count=("transport_mode", "size"))
            .sort_values("total_co2", ascending=False)
        )

        mode_co2["Label"] = mode_co2["transport_mode"].replace({
            "flight": "Flight",
            "train": "Train",
            "bus": "Bus",
            "rental_car": "Rental Car",
        })

        if mode_co2.empty:
            st.info("No transport mode data available for this selection.")
        else:
            mode_chart = (
                alt.Chart(mode_co2)
                .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
                .encode(
                    x=alt.X("Label:N", title="Transport Mode", sort="-y", axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("total_co2:Q", title="Total CO₂ Emissions (t)"),
                    color=alt.Color(
                        "Label:N",
                        scale=alt.Scale(
                            domain=["Flight", "Train", "Bus", "Rental Car"],
                            range=["#e05252", "#2cb67a", "#ffa73a", "#63acff"]
                        ),
                        legend=None,
                    ),
                    tooltip=[
                        alt.Tooltip("Label:N", title="Transport Mode"),
                        alt.Tooltip("total_co2:Q", title="Total CO₂ (t)", format=",.1f"),
                        alt.Tooltip("trip_count:Q", title="Number of Trips", format=","),
                    ],
                )
                .properties(title=f"CO₂ Emissions by Transport Mode – {analysis_subunit}", height=280)
            )

            st.download_button("⬇", data=mode_chart.to_html(), file_name="co2_transport_mode.html", mime="text/html", help="Download chart")
            st.altair_chart(mode_chart, use_container_width=True)

        # ── Block 3: cumulative over all years ────────────────────────────
        cumulative_df = df[df["year"] <= max_analysis_year].copy()

        if analysis_subunit != "All":
            cumulative_df = cumulative_df[cumulative_df["subunit"] == analysis_subunit]

        yearly_co2 = (
            cumulative_df.groupby("year", as_index=False)
            .agg(yearly_co2=("CO2e RFI2.7 (t)", "sum"))
            .sort_values("year")
        )

        if yearly_co2.empty:
            st.info("No CO₂ data available for the cumulative time series.")
        else:
            all_years = pd.DataFrame(
                {"year": list(range(int(df["year"].min()), max_analysis_year + 1))}
            )
            yearly_co2 = all_years.merge(yearly_co2, on="year", how="left")
            yearly_co2["yearly_co2"] = yearly_co2["yearly_co2"].fillna(0)
            yearly_co2["cumulative_co2"] = yearly_co2["yearly_co2"].cumsum()

            cumulative_chart = (
                alt.Chart(yearly_co2)
                .mark_line(point=alt.OverlayMarkDef(color="white", size=30, filled=True), strokeWidth=2, color="#2cb67a")
                .encode(
                    x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=-45)),
                    y=alt.Y("cumulative_co2:Q", title="Cumulative CO₂ Emissions (t)"),
                    tooltip=["year", "yearly_co2", "cumulative_co2"]
                )
                .properties(title="Cumulative CO₂ Emissions over the Years", height=300)
            )

            st.download_button("⬇", data=cumulative_chart.to_html(), file_name="co2_cumulative.html", mime="text/html", help="Download chart")
            st.altair_chart(cumulative_chart, use_container_width=True)

        # ==========================================
        # PREDICTION
        # ==========================================

        hist_df = df[df["year"] <= max_analysis_year].copy()
        if analysis_subunit != "All":
            hist_df = hist_df[hist_df["subunit"] == analysis_subunit]

        yearly_hist = (
            hist_df.groupby("year", as_index=False)
            .agg(co2=("CO2e RFI2.7 (t)", "sum"))
            .sort_values("year")
        )
        
        yearly_hist = yearly_hist.dropna(subset=["year", "co2"]) 
        trend_hist = yearly_hist[yearly_hist["year"] >= 2022].copy()

        if len(trend_hist) >= 2:
            
            n = len(trend_hist)
            x = trend_hist["year"].astype(float) - 2000
            y = trend_hist["co2"].astype(float)
            
            sum_x = x.sum()
            sum_y = y.sum()
            sum_x2 = (x**2).sum()
            sum_xy = (x*y).sum()
            
            divisor = (n * sum_x2 - sum_x**2)
            if divisor != 0:
                m = (n * sum_xy - sum_x * sum_y) / divisor
                b = (sum_y - m * sum_x) / n
            else:
                m, b = 0, 0
            
            future_years = [int(max_analysis_year) + 1, int(max_analysis_year) + 2, int(max_analysis_year) + 3]
            future_co2 = [max(0, m * (yr - 2000) + b) for yr in future_years] 

            future_df = pd.DataFrame({
                "year": future_years,
                "co2": future_co2
            })

            last_hist = yearly_hist.iloc[-1:].copy()
            pred_df = pd.concat([last_hist.assign(type="Prediction"), future_df.assign(type="Prediction")], ignore_index=True)
            hist_df_plot = yearly_hist.assign(type="Historical")
            plot_df = pd.concat([hist_df_plot, pred_df], ignore_index=True)

            pred_chart = (
                alt.Chart(plot_df)
                .mark_line(point=alt.OverlayMarkDef(color="white", size=30, filled=True), strokeWidth=2)
                .encode(
                    x=alt.X(
                        "year:O", 
                        title="Year", 
                        axis=alt.Axis(labelAngle=0)
                    ),
                    y=alt.Y("co2:Q", title="CO₂ Emissions (t)"),
                    color=alt.Color(
                        "type:N",
                        scale=alt.Scale(
                            domain=["Historical", "Prediction"],
                            range=["#63acff", "#ec082e"]
                        ),
                        legend=alt.Legend(title=None, orient="right", direction="vertical")
                    ),
                    strokeDash=alt.condition(
                        alt.datum.type == "Prediction",
                        alt.value([6, 4]),
                        alt.value([])
                    ),
                    tooltip=[
                        alt.Tooltip("year:O", title="Year"), 
                        alt.Tooltip("co2:Q", title="CO₂ Emissions (t)", format=",.1f"),
                        alt.Tooltip("type:N", title="Series")
                    ]
                )
                .properties(
                    title=f"Prediction of CO₂ Emissions – {analysis_subunit}",
                    height=280,
                )
            )
            st.download_button("⬇", data=pred_chart.to_html(), file_name="co2_prediction.html", mime="text/html", help="Download chart")
            st.altair_chart(pred_chart, use_container_width=True)
        else:
            st.info("Not enough historical data to generate a prediction. At least 2 years of data are required.")
        
        panel_end()

# ================================ Prediction End ===========================================

    with right:
        context_year = "All Years" if analysis_year == "All" else str(analysis_year)
        context_subunit = analysis_subunit
        
        dynamic_title = f"Analysis: {context_year} | {context_subunit}"
        
        panel_start(dynamic_title)

        total_trips = len(analysis_df)
        flight_count = len(analysis_df[analysis_df["transport_mode"] == "flight"])
        train_count = len(analysis_df[analysis_df["transport_mode"] == "train"])
        bus_count = len(analysis_df[analysis_df["transport_mode"] == "bus"])
        car_count = len(analysis_df[analysis_df["transport_mode"] == "rental_car"])

        st.markdown(
            f"""
            <div class="analysis-metric-grid">
                <div class="analysis-metric-card">
                    <div class="analysis-metric-label">Number of Trips</div>
                    <div class="analysis-metric-value">{format_int(total_trips)}</div>
                </div>
                <div class="analysis-metric-card">
                    <div class="analysis-metric-label">Number of Flights</div>
                    <div class="analysis-metric-value">{format_int(flight_count)}</div>
                </div>
                <div class="analysis-metric-card">
                    <div class="analysis-metric-label">Number of Trains</div>
                    <div class="analysis-metric-value">{format_int(train_count)}</div>
                </div>
                <div class="analysis-metric-card">
                    <div class="analysis-metric-label">Number of Buses</div>
                    <div class="analysis-metric-value">{format_int(bus_count)}</div>
                </div>
                <div class="analysis-metric-card">
                    <div class="analysis-metric-label">Number of Rental Cars</div>
                    <div class="analysis-metric-value">{format_int(car_count)}</div>
                </div>
                <div class="analysis-metric-card">
                    <div class="analysis-metric-label">CO₂ Emissions</div>
                    <div class="analysis-metric-value">{format_tonnes(analysis_df["CO2e RFI2.7 (t)"].sum())}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )



        analysis_purpose = (
            analysis_df.groupby("travel_purpose", as_index=False)
            .size()
            .rename(columns={"size": "Number"})
            .sort_values("Number", ascending=False)
        )

        if analysis_purpose.empty:
            st.info("No travel data available for this selection.")
        else:
            analysis_purpose["Label"] = analysis_purpose["travel_purpose"].str.replace("_", " ").str.title()

            total_num = analysis_purpose["Number"].sum()
            analysis_purpose["Percent"] = analysis_purpose["Number"] / total_num * 100

            analysis_purpose["Percent_Label"] = analysis_purpose["Percent"].apply(lambda x: f"{x:.0f}%" if x > 3 else "")

            base_analysis = alt.Chart(analysis_purpose).encode(
                theta=alt.Theta("Number:Q", stack=True),
                color=alt.Color(
                    "Label:N",
                    scale=alt.Scale(scheme="tableau10"
                        ),
                    legend=alt.Legend(title=None, orient="right"),
                ),
                tooltip=[
                    alt.Tooltip("Label:N", title="Travel Purpose"),
                    alt.Tooltip("Number:Q", format=",.0f"),
                    alt.Tooltip("Percent:Q", title="Share (%)", format=".1f"),
                ],
            )

            pie_analysis = base_analysis.mark_arc(innerRadius=0)
            text_analysis = base_analysis.mark_text(radius=75, fontSize=12, fontWeight="bold", fill="white").encode(
                text=alt.Text("Percent_Label:N")
            )

            final_analysis_pie = (pie_analysis + text_analysis).properties(height=250)

            st.download_button("⬇", data=final_analysis_pie.to_html(), file_name="travel_purposes.html", mime="text/html", help="Download chart")
            st.markdown('<div class="section-title" style="margin-top:-6px; margin-bottom:4px;">Travel Purposes</div>', unsafe_allow_html=True)
            st.altair_chart(final_analysis_pie, use_container_width=True)

        budget_years = sorted([y for y in budgets["year"].dropna().unique().tolist() if y <= max_analysis_year])
        
        # find the maximum percentage used across all years to set a common scale for the bars
        global_max_pct = 100.0
        for budget_year in budget_years:
            temp_budget = get_budget(budgets, analysis_subunit, budget_year)
            if temp_budget and temp_budget > 0:
                temp_used_df = df[df["year"] == budget_year].copy()
                if analysis_subunit != "All":
                    temp_used_df = temp_used_df[temp_used_df["subunit"] == analysis_subunit]
                temp_used = temp_used_df["CO2e RFI2.7 (t)"].sum()
                temp_pct = (temp_used / temp_budget) * 100
                if temp_pct > global_max_pct:
                    global_max_pct = temp_pct

        marker_pos = (100.0 / global_max_pct) * 100
                    
        # --------------------------------------------------------------------

        budget_rows_html = []
        budget_summary_rows = []

        for budget_year in budget_years:
            year_budget = get_budget(budgets, analysis_subunit, budget_year)
            year_used_df = df[df["year"] == budget_year].copy()
            
            if analysis_subunit != "All":
                year_used_df = year_used_df[year_used_df["subunit"] == analysis_subunit]

            year_used = year_used_df["CO2e RFI2.7 (t)"].sum()

            # NEU: Nur fortfahren, wenn ein Budget existiert (entfernt 2017-2019)
            if year_budget and year_budget > 0:
                year_pct = year_used / year_budget * 100
                
                # Berechnung der Balken-Breite basierend auf dem globalen Maximum
                year_width = (year_pct / global_max_pct) * 100
                marker_pos = (100.0 / global_max_pct) * 100
                
                percent_text = format_percent(year_pct)
                status_icon, status_text = get_status(year_pct)
                bar_color = get_bar_color(year_pct)
                
                # HTML für die Zeile generieren
                show_label = len(budget_rows_html) == 0
                label = f"<div style='position:absolute;top:-16px;left:{marker_pos}%;transform:translateX(-50%);font-size:10px;font-weight:700;color:white;white-space:nowrap;text-shadow:0 1px 3px rgba(0,0,0,0.8);'>100%</div>" if show_label else ""

                budget_rows_html.append(
                    f"""
                    <div class="budget-history-row">
                        <div class="budget-history-year">{int(budget_year)}</div>
                        <div class="budget-history-bg">
                            <div class="budget-history-fill" style="width:{year_width}%; background:{bar_color};"></div>
                            <div class="budget-marker" style="left:{marker_pos}%;"></div>
                        </div>
                        <div class="budget-history-percent">{percent_text}</div>
                        <div class="budget-status" style="font-size: 1.2rem;" title="{status_text}">{status_icon}</div>
                    </div>
                    """
                )

                # Daten für die Tabelle unten sammeln
                budget_summary_rows.append({
                    "year": int(budget_year),
                    "subunit": analysis_subunit,
                    "co2_budget_t": year_budget,
                    "co2_used_t": year_used,
                    "budget_used_percent": year_pct,
                    "status": status_text,
                })

        # Die gefilterten Balken anzeigen
        if budget_rows_html:
            budget_html_export = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
            <style>
                body {{ background: #0f172a; color: white; font-family: sans-serif; padding: 24px; }}
                .budget-history-row {{ display: grid; grid-template-columns: 55px 1fr 70px 34px; gap: 12px; align-items: center; margin-bottom: 12px; font-weight: 700; }}
                .budget-history-bg {{ height: 18px; background: rgba(255,255,255,0.18); border-radius: 8px; overflow: hidden; position: relative; }}
                .budget-history-fill {{ height: 100%; border-radius: 8px; }}
                .budget-marker {{ position: absolute; top: 0; bottom: 0; width: 3px; background-color: #ffffff; z-index: 10; }}
                .budget-history-percent {{ font-size: 15px; text-align: right; }}
                .budget-status {{ font-size: 18px; text-align: center; }}
                h2 {{ margin-bottom: 20px; }}
            </style></head><body>
            <h2>CO₂ Budget Limits – {analysis_subunit}</h2>
            <div style='display:grid;grid-template-columns:55px 1fr 70px 34px;gap:12px;margin-bottom:2px;'>
                <div></div>
                <div style='position:relative;height:14px;'>
                    <div style='position:absolute;left:{marker_pos}%;transform:translateX(-50%);font-size:11px;font-weight:700;color:white;white-space:nowrap;'>100%</div>
                </div><div></div><div></div>
            </div>
            {"".join(budget_rows_html)}
            </body></html>"""

            st.download_button("⬇", data=budget_html_export, file_name="co2_budget_limits.html", mime="text/html", help="Download chart")
            st.markdown('<div class="section-title" style="margin-top:-6px; margin-bottom:4px;">CO₂ Budget Limits</div>', unsafe_allow_html=True)
            st.markdown(
                f"<div style='display:grid;grid-template-columns:55px 1fr 70px 34px;gap:12px;margin-bottom:2px;'>"
                f"<div></div>"
                f"<div style='position:relative;height:14px;'>"
                f"<div style='position:absolute;left:{marker_pos}%;transform:translateX(-50%);font-size:11px;font-weight:700;color:white;white-space:nowrap;text-shadow:0 1px 3px rgba(0,0,0,0.8);'>100%</div>"
                f"</div><div></div><div></div></div>",
                unsafe_allow_html=True
            )
            st.markdown("".join(budget_rows_html), unsafe_allow_html=True)
        else:
            st.info("No budget data available for the selected filters.")

        budget_summary = pd.DataFrame(budget_summary_rows)

        st.markdown('<div style="height:48px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Budget Summary Table</div>', unsafe_allow_html=True)

        show_budget_summary = budget_summary.copy()
        show_budget_summary["co2_budget_t"] = show_budget_summary["co2_budget_t"].map(
            lambda x: round(x, 1) if pd.notna(x) else None
        )
        show_budget_summary["co2_used_t"] = show_budget_summary["co2_used_t"].map(
            lambda x: round(x, 1) if pd.notna(x) else None
        )
        show_budget_summary["budget_used_percent"] = show_budget_summary["budget_used_percent"].map(
            lambda x: round(x, 1) if pd.notna(x) else None
        )

        st.dataframe(show_budget_summary, use_container_width=True, hide_index=True, key="budget_summary_table")

        panel_end()

    