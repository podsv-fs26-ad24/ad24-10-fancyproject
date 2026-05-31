
# ===========================================================================================
# TRAVEL INSIGHTS DASHBOARD - Streamlit App
# ===========================================================================================
# This code sets up a Streamlit application for a Travel Insights Dashboard, which visualizes 
# travel data and CO2 budgets. 
#
# Features:
# - Custom CSS styling for a dark theme.
# - Functions to load and preprocess data from an Excel file.
# - Two main views: 
#   1. Overview: Shows current year travel costs and CO2 usage against budgets.
#   2. Analysis: Allows users to explore trends over multiple years.
#
# The code is structured to be modular and maintainable, separating data handling, 
# presentation logic, and UI components.

# Latest version 03.05-26, better than travel_dashboard

# ===========================================================================================
# ===========================================================================================



# =========================
# --- SETUP & IMPORTS ---
# =========================

import streamlit as st                          # Web application interface
import pandas as pd                             # Data manipulation and analysis
import altair as alt                            # Generating charts and visualizations
from pathlib import Path                        # to handle cross-platform file paths
from datetime import date                       # to fetch and format today's date

# Set the initial configuration for the Streamlit page
st.set_page_config(                           
    page_title="Travel Insights Dashboard",    
    page_icon="✈️",                            
    layout="wide",                              # wide layout to maximize screen space
)

# Define the path to the Excel data file dynamically based on the script's location
DATA_FILE = Path(__file__).parent.parent / "data_acquisition" / "traveldata-export.xlsx"




# =============================
# --- CUSTOM STYLING (CSS) ---
# =============================
# Injects custom CSS to override Streamlit's default theme, applying a dark UI, custom selectboxes, buttons, tooltips, and table formatting.


# Inject custom CSS for dark theme and UI component styling
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


# ========================
# ---- DATA LOADING ------
# ========================
# Reads the travel data and CO₂ budgets from the Excel file and preprocesses them. 
# Columns are converted into the correct data types (e.g., text to date formats or numbers) so they can be calculated without errors later on.

@st.cache_data
def load_data(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Reads travel and CO2 budget data from an Excel file and preprocesses it.
    Dates are converted, numeric values are coerced, and strings are cleaned 
    to ensure seamless integration with pandas and Altair.
    """
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



# ==========================
# --- HELPER FUNCTIONS ---
# ==========================
# The following helper functions are defined to format numerical values for display, manage the layout of section panels, calculate budget usage, and determine 
# visual indicators based on budget status.

def format_chf(x: float) -> str:
    """Formats a number as Swiss Francs (CHF) with apostrophe thousands separators."""
    return f"{x:,.0f} CHF".replace(",", "’")


def format_tonnes(x: float) -> str:
    """Formats a number as metric tonnes (t) with one decimal place."""
    if x is None or pd.isna(x):
        return "-"
    return f"{x:,.1f} t".replace(",", "’")


def format_percent(x: float) -> str:
    """Formats a number as a percentage string."""
    if x is None or pd.isna(x):
        return "-"
    return f"{x:.0f}%"


def format_int(x: float) -> str:
    """Formats large integers using apostrophes as thousands separators."""
    return f"{int(round(x)):,}".replace(",", "’")


def panel_start(title: str):
    """Generates the starting HTML layout for a styled dashboard section panel."""
    st.markdown('<div class="section-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def panel_end():
    """Closes the HTML layout for a dashboard section panel."""
    st.markdown("</div>", unsafe_allow_html=True)


def get_budget(budgets_df: pd.DataFrame, selected_subunit: str, selected_year: int) -> float | None:
    """
    Retrieves the total CO2 budget for a specific organizational subunit and year.
    Returns None if no data is found to handle missing historical budgets gracefully.
    """
    b = budgets_df[budgets_df["year"] == selected_year].copy()
    if selected_subunit != "All":
        b = b[b["subunit"] == selected_subunit]

    valid = b["co2_budget_t"].dropna()
    if valid.empty:
        return None
    return valid.sum()


def get_status(pct: float) -> tuple[str, str]:
    """Returns an emoji and status text based on the budget usage percentage."""
    if pct is None or pd.isna(pct):
        return "➖", "No budget"
    if pct > 100:
        return "❌", "Over budget"
    if pct >= 80:
        return "⚠️", "Critical"
    return "✅", "Within budget"


def get_bar_color(pct: float) -> str:
    """Returns a CSS linear-gradient string depending on budget threshold limits."""
    if pct is None or pd.isna(pct):
        return "rgba(255,255,255,0.18)"
    if pct > 100:
        return "linear-gradient(90deg, #dc2626, #991b1b)"
    if pct >= 80:
        return "linear-gradient(90deg, #f7941d, #d97706)"
    return "linear-gradient(90deg, #2e7d32, #1b5e20)"


def altair_theme() -> dict:
    """Registers and returns a custom dark theme configuration for Altair charts."""
    return {
        "config": {
            "background": "#172133",
            "view": {"stroke": "transparent", "fill": "#172133"},
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
            "title": {
                "color": "white",
                "fontSize": 28,
                "anchor": "start",
                "offset": 15
            },
        },
    }

alt.themes.register("travel_dark", altair_theme)
alt.themes.enable("travel_dark")

# ==========================
# --- SESSION STATE ---
# ==========================
# The session state is used to keep track of the current view (Overview or Analysis) across user interactions.

if "dashboard_view" not in st.session_state:        # Check if view state is initialized
    st.session_state.dashboard_view = "Overview"    # Initialize to 'Overview' view



# =========================
# --- GLOBAL OPTIONS ---
# =========================
# The following code dynamically generates lists of unique years, subunits, departure and arrival locations from the loaded data, which are used to populate filter options in the dashboard.

current_year = 2025                 # Set the current reporting year
max_analysis_year = 2025            # Set the maximum year allowed for analysis

# Dynamically extract unique values to populate UI filters
year_options = ["All"] + sorted([y for y in df["year"].dropna().unique().tolist() if y <= max_analysis_year], reverse=True)
subunit_options = ["All"] + sorted(df["subunit"].dropna().unique().tolist())                                                
all_departures = ["All"] + sorted(df["departure_iata"].dropna().unique().tolist())                                          
all_arrivals = ["All"] + sorted(df["arrival_iata"].dropna().unique().tolist())                                              
#used_co2 = 0




# =========================
# --- HEADER -- -
# ========================
# The header section of the dashboard is structured using Streamlit's column layout to create a visually balanced header with the main title and year on the left, 
# and navigation buttons and today's date on the right.

# callback function to change the current view in session state when a navigation button is clicked
def change_view(view_name):
    st.session_state.dashboard_view = view_name

header_left, header_right = st.columns([6, 2.2]) # Define header columns

# dynamic header text based on current view and selected year in session state
if st.session_state.dashboard_view == "Overview":
    header_year_text = f"Year {current_year}"
else:
    # Analysis view: show selected year or "All Years" if no specific year is selected
    selected_year = st.session_state.get("analysis_year", "All")
    header_year_text = f"Year {selected_year}" if selected_year != "All" else "All Years"

with header_left:
    st.markdown(                                                            # Display dashboard title and dynamic year
        f"<h1 style='text-align:left; margin-top:0.4rem; margin-bottom:0;'>Travel Insights Dashboard</h1>"
        f"<div style='font-size: 2rem; font-weight: 600; color: rgba(255,255,255,0.8); margin-top: 2px;'>{header_year_text}</div>",
        unsafe_allow_html=True,
    )

with header_right:
    st.markdown('<div class="small-filter-box" style="margin-bottom: 5px;">', unsafe_allow_html=True)   # Open filter box HTML
    
    b1, b2 = st.columns(2)                # Create columns for navigation buttons
    with b1:
        # On click and args are used to update the session state when a button is clicked, instead of relying on if st.button() which can lead to issues with multiple buttons
        st.button("Overview", use_container_width=True, on_click=change_view, args=("Overview",))
    with b2:
        # On click and args to update the session state when a button is clicked
        st.button("Analysis", use_container_width=True, on_click=change_view, args=("Analysis",))

    st.markdown("</div>", unsafe_allow_html=True)                           # Close filter box HTML
    
    st.markdown(                                                            # Display current dynamic date
        f"<div class='date-box' style='padding-right: 10px;'>TODAY: {date.today().strftime('%d.%m.%Y')}</div>",
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)                                 # Display horizontal line divider

# ===============================
# --- OVERVIEW DASHBOARD VIEW ---
# ===============================
# Provides a high-level summary of travel data for the selected year and subunit, detailing total CO2 emissions against organizational budgets and analyzing 
# standard travel routes.

if st.session_state.dashboard_view == "Overview":

    filter_col, spacer = st.columns([1.25, 4.75])                                                   # Create layout for subunit selector

    with filter_col:
        subunit = st.selectbox("Choose Subunit", subunit_options, index=0, key="overview_subunit")  # Display subunit dropdown

    overview_df = df[df["year"] == current_year].copy()                                             # Filter data for current year

    if subunit != "All":
        overview_df = overview_df[overview_df["subunit"] == subunit]                                # Filter data for selected subunit

    used_co2 = overview_df["CO2e RFI2.7 (t)"].sum()                                                 # Calculate used CO2
    travel_cost = overview_df["cost_CHF"].sum()                                                     # Calculate travel costs
    total_company_cost = df[df["year"] == current_year]["cost_CHF"].sum()                           # Calculate total company costs
    subunit_share = (travel_cost / total_company_cost * 100) if total_company_cost > 0 else 0       # Calculate subunit cost share
    budget = get_budget(budgets, subunit, current_year)                                             # Get subunit budget
    usage_pct = (used_co2 / budget * 100) if budget and budget > 0 else None                        # Calculate percentage of budget used
    
    # Dynamic scaling 
    if usage_pct is not None:
        max_scale = max(100.0, usage_pct)                   # Scale the bar to at least 100% to accommodate over-budget scenarios
        progress_width = (usage_pct / max_scale) * 100      # Set bar width
        marker_pos = (100.0 / max_scale) * 100              # Set 100% marker position
    else:
        progress_width = 0                                  # Default width
        marker_pos = 100                                    # Default marker position

    left, right = st.columns([1, 1.15], gap="large")        # Split main body into two columns


    # ────────────────── Left Overview Panel ──────────────
    with left:
        panel_start(f"Subunit Overview {current_year}")

        if budget and budget > 0:
            progress_color = get_bar_color(usage_pct)           # Retrieve gradient color

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
            """                                                 # Construct HTML for custom progress bar

            st.markdown(budget_html, unsafe_allow_html=True)    # Render custom progress bar

        else:
            st.warning("For this subunit, no CO₂ budget was found for the year 2025.")  # Warning if no budget

        if subunit != "All":
            cost_context = f"{subunit_share:.1f}% of total company travel costs"        # Text for specific subunit
        else:
            cost_context = "Total company travel costs"                                 # Text for whole company

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
    )                                                                               # Render custom travel costs box

    # ────────────────── Right Overview Panel ──────────────
    with right:
        panel_start("Travel Options")

        route_col1, route_col2 = st.columns(2)                                      # Sub-columns for dropdowns

        with route_col1:
            departure = st.selectbox("Departure Location", all_departures, index=0) # Departure dropdown

        with route_col2:
            arrival = st.selectbox("Arrival Location", all_arrivals, index=0)       # Arrival dropdown

        route_df = df.copy()                                                        # Copy full dataset for route analysis

        if departure != "All":
            route_df = route_df[route_df["departure_iata"] == departure]            # Filter by departure

        if arrival != "All":
            route_df = route_df[route_df["arrival_iata"] == arrival]                # Filter by arrival

        st.markdown(
            f"""
            <div style="margin:10px 0 12px 0; font-weight:600;">
                Data Basis: <span style="color:#dfe9ff;">all years</span><br>
                Route: <span style="color:#dfe9ff;">{departure if departure != "All" else "all departure locations"} → {arrival if arrival != "All" else "all destination locations"}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )                                                                           # Render route context text

        if departure == "All" or arrival == "All":
            st.info("Please select a departure and destination location.")          # Instruction message
        elif route_df.empty:
            st.warning("No data available for this route.")                         # Warning if route is empty
        else:
            summary = (
                route_df.groupby("transport_mode", as_index=False)                  # Group by transport mode
                .agg(
                    trips=("transport_mode", "size"),                               # Count trips
                    avg_cost=("cost_CHF", "mean"),                                  # Get mean cost
                    avg_co2_t=("CO2e RFI2.7 (t)", "mean"),                          # Get mean CO2
                    avg_km=("km", "mean"),                                          # Get mean distance
                )
            )

            mode_order = ["flight", "train", "bus", "rental_car"]                   # Logical sorting order
            summary["sort"] = summary["transport_mode"].apply(
                lambda x: mode_order.index(x) if x in mode_order else 99
            )                                                                       # Apply sorting index
            summary = summary.sort_values("sort").drop(columns="sort")              # Sort and clean up

            summary["Option"] = summary["transport_mode"].replace(
                {
                    "flight": "Flight",
                    "train": "Train",
                    "bus": "Bus",
                    "rental_car": "Rental Car",
                }
            )                                                                       # Capitalize labels

            summary["Ø cost"] = summary["avg_cost"].map(lambda x: format_chf(x) if pd.notna(x) else "-")                        # Format costs
            summary["Ø CO₂"] = summary["avg_co2_t"].map(lambda x: f"{x*1000:.0f} kg" if pd.notna(x) else "-")                   # Format CO2 to kg
            summary["Ø distance"] = summary["avg_km"].map(lambda x: f"{x:,.0f} km".replace(",", "’") if pd.notna(x) else "-")   # Format distance

            min_cost = summary["avg_cost"].min() # Find lowest cost
            min_co2 = summary["avg_co2_t"].min() # Find lowest CO2

            def recommendation(row):
                tags = []
                if row["avg_cost"] == min_cost:
                    tags.append("cheapest")                                   # Tag cheapest
                if row["avg_co2_t"] == min_co2:
                    tags.append("most environmentally friendly")              # Tag greenest
                if not tags:
                    return "—"                                                # Return blank if neither
                return ("Cheapest & most environmentally friendly option"
                        if len(tags) == 2
                        else tags[0].capitalize() + " option")                # Return combined or single tag string

            summary["recommendation"] = summary.apply(recommendation, axis=1) # Apply recommendation logic

            show_df = summary[
                ["Option", "trips", "Ø distance", "Ø cost", "Ø CO₂", "recommendation"]
            ].rename(columns={"trips": "Number of Trips"})                    # Select columns and rename

            st.table(show_df)                                                 # Render Streamlit table

        panel_end()

# ================================
# --- ANALYSIS DASHBOARD VIEW ---
# ================================
# The Analysis view allows users to explore trends in CO2 emissions over time, with the ability to filter by year and subunit. 
# It includes an interactive line chart showing cumulative CO2 emissions by month, with a reference line for the CO2 budget if available.

else:
    filter_col1, filter_col2, spacer = st.columns([1.2, 1.4, 3.4])                                              # Create columns for top filters

    with filter_col1:
        analysis_year = st.selectbox("Choose Year", year_options, index=0, key="analysis_year")                 # Render year filter

    with filter_col2:
        analysis_subunit = st.selectbox("Choose Subunit", subunit_options, index=0, key="analysis_subunit")     # Render subunit filter

    analysis_df = df[df["year"] <= max_analysis_year].copy()                                                    # Filter out future years


    # Apply dimensional filters sequentially. Applying time filters prior to 
    # structural filters optimizes performance for larger datasets.
    if analysis_year != "All":
        analysis_df = analysis_df[analysis_df["year"] == analysis_year]                                         # Apply year filter

    if analysis_subunit != "All":
        analysis_df = analysis_df[analysis_df["subunit"] == analysis_subunit]                                   # Apply subunit filter

    left, right = st.columns([1.15, 1], gap="large")                                                            # Split main body into two columns

    # ────────────────── Left Analysis Panel ──────────────────
    with left:
        st.markdown('<div class="section-panel">', unsafe_allow_html=True)                                      # Open styled panel

        if analysis_year == "All":
            line_year = current_year                                                                            # Default to current year for line chart
        else:
            line_year = int(analysis_year)                                                                      # Use selected year


        # ────────── Cumulative Current Year ───────────
        # This block generates the data and line chart for the cumulative CO2 emissions over the months of the selected year, applying the necessary filters and aggregations.
        # It also checks for the existence of data and budget information to conditionally render the chart with or without the budget reference line.


        line_df = df[(df["year"] == line_year) & (df["year"] <= max_analysis_year)].copy() # Isolate data for the line chart year

        # Check if a specific year is selected to ensure the line chart reflects the user's choice. 
        if analysis_subunit != "All": 
            line_df = line_df[line_df["subunit"] == analysis_subunit] # Apply subunit filter

        line_df = (                                         # Start aggregation
            line_df.groupby("month", as_index=False)        # Group data by month
            .agg(monthly_co2=("CO2e RFI2.7 (t)", "sum"))    # Sum CO2 per month
            .sort_values("month")                       
        )

        # Checks if there is any data available for the selected year and subunit. 
        if line_df.empty:                                        
            st.info("No data available for the yearly trend.")     
                
        else:
            all_months = pd.DataFrame(                                          # Create dataframe with all 12 months
                {"month": pd.date_range(start=f"{line_year}-01-01", end=f"{line_year}-12-01", freq="MS")} # Generate monthly dates
            )
            line_df = all_months.merge(line_df, on="month", how="left")         # Merge to ensure missing months are included
            line_df["monthly_co2"] = line_df["monthly_co2"].fillna(0)           # Fill missing month data with 0
            line_df["cumulative_co2"] = line_df["monthly_co2"].cumsum()         # Calculate cumulative CO2 sum

            line_budget = get_budget(budgets, analysis_subunit, line_year)      # Retrieve budget for the line chart year

            co2_line = (                    # Generate Altair line chart
                alt.Chart(line_df)          # Pass data to chart
                .mark_line(point=alt.OverlayMarkDef(color="white", size=30, filled=True), strokeWidth=2, color="#ffa73a")       # Add line with dots
                .encode(                                                                                                          # Configure axes
                    x=alt.X("month:T", title="Month", axis=alt.Axis(format="%b", labelAngle=0)),                                  # X-axis as time
                    y=alt.Y("cumulative_co2:Q", title="Cumulative CO₂ Emissions (t)"),                                            # Y-axis as quantitative
                    tooltip=[                                                                                                     # Add interactive tooltips
                        alt.Tooltip("month:T", title="Month", format="%b %Y"),                                                    
                        alt.Tooltip("monthly_co2:Q", title="CO₂ in Month (t)", format=",.1f"),                                    
                        alt.Tooltip("cumulative_co2:Q", title="CO₂ Cumulative (t)", format=",.1f"),                               
                    ],
                )
            )

            # Budget line and label are only added to the chart if a valid budget exists for the selected year and subunit.
            if line_budget and line_budget > 0:                                         # Check if budget line is needed
                budget_rule_data = pd.DataFrame({"budget": [line_budget]})              # Create data for budget rule
                budget_rule = (                                                         # Generate budget line
                    alt.Chart(budget_rule_data)                                        
                    .mark_rule(color="#dc2626", strokeWidth=3, strokeDash=[6, 4])     # Style as dashed red line
                    .encode(y="budget:Q", tooltip=[alt.Tooltip("budget:Q", title="Budget limit (t)", format=",.1f")]) # Set Y position and tooltip
                )
                budget_label = (                                                        # Generate text label for budget line
                    alt.Chart(budget_rule_data) 
                    .mark_text(align="left", baseline="bottom", dy=-6, color="#dc2626", fontWeight=600, fontSize=13)    # Style text label
                    .encode(y="budget:Q", x=alt.value(10), text=alt.value(f'Budget limit {line_budget:,.1f} t'))          # Set position and content
                )
                line_chart = (co2_line + budget_rule + budget_label).properties(title=f"Cumulative CO₂ Emissions {line_year} – {analysis_subunit}", height=330) # Combine elements
            
            # If no valid budget exists, the chart is rendered without the budget line and label, and the title is adjusted accordingly 
            else: 
                line_chart = co2_line.properties(title=f"Cumulative CO₂ Emissions {line_year} – {analysis_subunit}", height=330)           # Display just the line chart

            st.download_button("⬇", data=line_chart.to_html(), file_name="co2_yearly_trend.html", mime="text/html", help="Download chart") # Render download button
            st.altair_chart(line_chart, use_container_width=True) # Render Altair chart in Streamlit


        # ─────────────────────────────── CO₂ by Transport Mode ───────────────────────────────
        # This block generates a bar chart showing total CO2 emissions by transport mode for the selected year and subunit, 
        # allowing users to compare the environmental impact of different travel options.

        mode_df = df[df["year"] <= max_analysis_year].copy()         # Filter data for mode analysis

        # Year filter is applied first to narrow down the dataset to the relevant time frame before applying the subunit filter = improves performance
        if analysis_year != "All":
            mode_df = mode_df[mode_df["year"] == int(analysis_year)]

        # Subunit filter is applied after the year filter to ensure that the dataset is narrowed down to the relevant time frame before filtering by organizational unit.
        if analysis_subunit != "All":
            mode_df = mode_df[mode_df["subunit"] == analysis_subunit]

        mode_co2 = (                                                # Aggregate data by transport mode
            mode_df.groupby("transport_mode", as_index=False)     
            .agg(total_co2=("CO2e RFI2.7 (t)", "sum"), trip_count=("transport_mode", "size")) # Sum CO2 and count trips
            .sort_values("total_co2", ascending=False)             
        )

        mode_co2["Label"] = mode_co2["transport_mode"].replace({    # Clean up labels for display
            "flight": "Flight",                              
            "train": "Train",                                
            "bus": "Bus",                                          
            "rental_car": "Rental Car",                            
        })

        # checks if there is any data available for the transport mode analysis.
        # If data is available, it proceeds to generate a bar chart that visualizes the total CO2 emissions by transport mode for the selected year and subunit.
        if mode_co2.empty:  
            st.info("No transport mode data available for this selection.")        
        
        # if available --> generates bar chart using Altair
        else:
            # Calculate the max CO2 value
            max_co2 = mode_co2["total_co2"].max()
            if pd.isna(max_co2) or max_co2 == 0:
                max_co2 = 100 

            # Creates String : "1,556 t  /   15 Trips"
            mode_co2["bar_label"] = mode_co2.apply(
                lambda x: f"{x['total_co2']:,.0f} t   /    {x['trip_count']} Trips", axis=1
            )
            # -------------------------------------------------------

            # 1. Basic chart setup with axes and scales
            base = alt.Chart(mode_co2).encode(
                y=alt.Y("Label:N", title=None, sort="-x", axis=alt.Axis(labelAngle=0, labelFontSize=13, grid=False)), 
                
                # Scale the x-axis by adding a 35% margin to the maximum CO2 value to ensure labels fit without overlap
                x=alt.X("total_co2:Q", 
                        title="Total CO₂ Emissions (t)", 
                        axis=alt.Axis(grid=True),
                        scale=alt.Scale(domain=[0, max_co2 * 1.35]) 
                ),
            )

            # 2. Draw the horizontal bars
            bars = base.mark_bar(
                cornerRadiusTopRight=4,    
                cornerRadiusBottomRight=4, 
                size=30                    
            ).encode(
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
                ]
            )

            # 3. Add text labels at the end of each bar to show the exact CO2 values, formatted with thousands separators for better readability.
            text = base.mark_text(
                align='left',     
                baseline='middle',
                dx=8,             # Offset to the right of the bar end
                color="white",
                fontSize=13,
                fontWeight=600
            ).encode(
                # we use the pre-formatted 'bar_label' column for the text to ensure consistent formatting and avoid issues with large numbers in tooltips
                text=alt.Text("bar_label:N") 
            )

            # 4. Layer the bars and text
            mode_chart = (bars + text).properties(
                title=f"CO₂ Emissions by Transport Mode – {analysis_subunit}", 
                height=280
            )
            st.download_button("⬇", data=mode_chart.to_html(), file_name="co2_transport_mode.html", mime="text/html", help="Download chart") # Render download button
            st.altair_chart(mode_chart, use_container_width=True) # Render Altair chart in Streamlit


        # ────────────── Cumulative Over All Years ────────────────────────────
        # This block generates a line chart showing the cumulative CO2 emissions over all years up to the maximum analysis year.
        
        cumulative_df = df[df["year"] <= max_analysis_year].copy()      # Filter data for overall cumulative analysis

        if analysis_subunit != "All":                                   # Check subunit filter
            cumulative_df = cumulative_df[cumulative_df["subunit"] == analysis_subunit] # Apply subunit filter

        yearly_co2 = (                                      # Aggregate total CO2 per year 
            cumulative_df.groupby("year", as_index=False) 
            .agg(yearly_co2=("CO2e RFI2.7 (t)", "sum"))     # Sum CO2 per year
            .sort_values("year")                         
        )

        if yearly_co2.empty:                                # Check if data exists for cumulative chart
            st.info("No CO₂ data available for the cumulative time series.")
        else:                                         
            all_years = pd.DataFrame(                       # Create full range of years to fill gaps 
                {"year": list(range(int(df["year"].min()), max_analysis_year + 1))} # List all years from min to max analysis year
            )
            yearly_co2 = all_years.merge(yearly_co2, on="year", how="left")     # Merge missing years into dataframe 
            yearly_co2["yearly_co2"] = yearly_co2["yearly_co2"].fillna(0)       # Fill gaps with 0 for accurate cumulative calculation
            yearly_co2["cumulative_co2"] = yearly_co2["yearly_co2"].cumsum()    # Calculate multi-year cumulative sum 

            cumulative_chart = (                # Generate line chart for cumulative CO2 over years 
                alt.Chart(yearly_co2)           # Pass data to chart 
                .mark_line(point=alt.OverlayMarkDef(color="white", size=30, filled=True), strokeWidth=2, color="#2cb67a") # Style line and points 
                .encode(                                                                    # Configure axes and tooltips to show year, yearly CO2, and cumulative CO2
                    x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=-45)),         # X-axis ordinal (years) 
                    y=alt.Y("cumulative_co2:Q", title="Cumulative CO₂ Emissions (t)"),      # Y-axis quantitative 
                    tooltip=["year", "yearly_co2", "cumulative_co2"]                        # Set tooltips 
                )
                .properties(title="Cumulative CO₂ Emissions over the Years", height=300)    # Set title and height 
            )

            st.download_button("⬇", data=cumulative_chart.to_html(), file_name="co2_cumulative.html", mime="text/html", help="Download chart") # Render download button 
            st.altair_chart(cumulative_chart, use_container_width=True)                     # Render Altair chart in Streamlit 

        # ──────────────────────── PREDICTION  ────────────────────────
        # This block performs a simple linear regression on the historical CO2 emissions data from 2022 onwards to predict future emissions for the next three years.
        # The linear regression formula is based on the least squares method, where 'm' represents the slope of the line (the rate of change of CO2 emissions per year) 
        # and 'b' represents the y-intercept (the estimated CO2 emissions at the year 2000 in this normalized scale).

        hist_df = df[df["year"] <= max_analysis_year].copy()            # Get historical data
        if analysis_subunit != "All":                                   # Apply subunit filter
            hist_df = hist_df[hist_df["subunit"] == analysis_subunit]   # Filter by subunit

        yearly_hist = (                                                 # Aggregate historical data by year
            hist_df.groupby("year", as_index=False)                     # Group by year
            .agg(co2=("CO2e RFI2.7 (t)", "sum"))                        # Sum CO2
            .sort_values("year")                                        # Sort chronologically
        )
        
        yearly_hist = yearly_hist.dropna(subset=["year", "co2"])        # Remove empty rows
        trend_hist = yearly_hist[yearly_hist["year"] >= 2022].copy()    # Filter for recent years for trend line

        if len(trend_hist) >= 2:                                        # Require at least 2 data points for linear regression
            
            n = len(trend_hist)                                         # Get number of data points
            x = trend_hist["year"].astype(float) - 2000                 # Normalize x (years) for calculation to avoid large numbers
            y = trend_hist["co2"].astype(float)                         # Get y values (CO2)
            
            sum_x = x.sum()             
            sum_y = y.sum()             
            sum_x2 = (x**2).sum()       
            sum_xy = (x*y).sum()        
            
            divisor = (n * sum_x2 - sum_x**2)               # calculate denominator for slope formula
            if divisor != 0:                                # Avoid division by zero
                m = (n * sum_xy - sum_x * sum_y) / divisor  
                b = (sum_y - m * sum_x) / n                
    
            
            # If divisor is zero, we cannot calculate a slope or intercept, so we default to a flat line with zero slope and intercept at zero.
            else: 
                m, b = 0, 0     # Default to 0
            
            future_years = [int(max_analysis_year) + 1, int(max_analysis_year) + 2, int(max_analysis_year) + 3]     # Generate next 3 years 
            future_co2 = [max(0, m * (yr - 2000) + b) for yr in future_years]                                       # Calculate predicted CO2 (ensuring it's not below 0) 

            future_df = pd.DataFrame({              # Create dataframe for predictions 
                "year": future_years,               
                "co2": future_co2              
            })

            last_hist = yearly_hist.iloc[-1:].copy()                        # Get the last historical point to connect the lines 
            pred_df = pd.concat([last_hist.assign(type="Prediction"), future_df.assign(type="Prediction")], ignore_index=True) # Create prediction dataset with type label for styling
            hist_df_plot = yearly_hist.assign(type="Historical")            # Label historical dataset
            plot_df = pd.concat([hist_df_plot, pred_df], ignore_index=True) # Combine both datasets

            pred_chart = (                                                                               # Generate prediction chart 
                alt.Chart(plot_df)                                                                       # Pass combined data to chart
                .mark_line(point=alt.OverlayMarkDef(color="white", size=30, filled=True), strokeWidth=2) # Style lines and points 
                .encode(                                                                                 # Configure axes and visual properties 
                    x=alt.X(
                        "year:O", 
                        title="Year", 
                        axis=alt.Axis(labelAngle=0)                 # X-axis year without rotation 
                    ),
                    y=alt.Y("co2:Q", title="CO₂ Emissions (t)"),    # Y-axis quantitative for CO2 emissions
                    color=alt.Color(                                # Color lines 
                        "type:N",                                   # Type nominal for color encoding 
                                                                    #   - N => Nominal      (categorical variable, used for coloring and styling)
                                                                    #   - C => Categorical  (inherent order, used for coloring and styling)
                                                                    #   - Q => Quantitative (numerical variable, used for axes and sizing)
                        scale=alt.Scale(                            # Map specific colors to historical and prediction 
                            domain=["Historical", "Prediction"],    # Categories 
                            range=["#63acff", "#ec082e"]        
                        ),
                        legend=alt.Legend(title=None, orient="right", direction="vertical") # Format legend 
                    ),
                    strokeDash=alt.condition(                       # Apply dashed line to predictions 
                        alt.datum.type == "Prediction",             # Condition check 
                        alt.value([6, 4]),                          # Dashed line if true 
                        alt.value([])                               # Solid line if false
                    ),
                    tooltip=[                                       # Set Tooltips
                        alt.Tooltip("year:O", title="Year"),        
                        alt.Tooltip("co2:Q", title="CO₂ Emissions (t)", format=",.1f"), 
                        alt.Tooltip("type:N", title="Series")       
                    ]
                )
                .properties(
                    title=f"Prediction of CO₂ Emissions – {analysis_subunit}", # Dynamic title based on subunit
                    height=280, 
                )
            )
            st.download_button("⬇", data=pred_chart.to_html(), file_name="co2_prediction.html", mime="text/html", help="Download chart") # Render download button
            st.altair_chart(pred_chart, use_container_width=True) # Render Altair chart
        
        # If insufficient data points exist to calculate a trend line, inform the user that a prediction cannot be generated and that at least 2 years of data are required for the linear regression.
        else:
            st.info("Not enough historical data to generate a prediction. At least 2 years of data are required.")
        
        panel_end() # Close left panel

# ────────────────────────────────── RIGHT ANALYSIS PANEL ──────────────────────────────────
# Renders a dynamic summary for the selected year and subunit.
# Includes a KPI grid (trips, transport modes, CO2), a pie chart for travel purposes, 
# and a historical budget tracking visualization to show long-term emission trends.

    with right:                                      
        context_year = "All Years" if analysis_year == "All" else str(analysis_year) # Create dynamic title string for year
        context_subunit = analysis_subunit                              # Create dynamic title string for subunit
        
        dynamic_title = f"Analysis: {context_year} | {context_subunit}" # Combine strings into panel title
        
        panel_start(dynamic_title)   

        total_trips = len(analysis_df)                                                
        flight_count = len(analysis_df[analysis_df["transport_mode"] == "flight"])    
        train_count = len(analysis_df[analysis_df["transport_mode"] == "train"])      
        bus_count = len(analysis_df[analysis_df["transport_mode"] == "bus"])          
        car_count = len(analysis_df[analysis_df["transport_mode"] == "rental_car"])   

        # render a grid of key metrics at the top of the right panel, showing total trips, counts for each transport mode, 
        # and total CO2 emissions for the selected year and subunit.
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



        analysis_purpose = (            # Group and aggregate data by travel purpose 
            analysis_df.groupby("travel_purpose", as_index=False)       
            .size()                                                      # Count occurrences of each purpose 
            .rename(columns={"size": "Number"})                          # Rename count column to "Number" for clarity
            .sort_values("Number", ascending=False)                      # Sort descending by number of trips for better visualization in the pie chart
        )

        # check if there is any data available for the travel purpose breakdown.    
        if analysis_purpose.empty:                                     
            st.info("No travel data available for this selection.")   
        
        # If data is available, it proceeds to generate a pie chart that visualizes the distribution of travel purposes for the selected year and subunit.
        else: 
            analysis_purpose["Label"] = analysis_purpose["travel_purpose"].str.replace("_", " ").str.title()    # clean up Labels

            total_num = analysis_purpose["Number"].sum()                                                        # total number of trips for percentage calculation
            analysis_purpose["Percent"] = analysis_purpose["Number"] / total_num * 100                          # Calculate percentage for each purpose

            analysis_purpose["Percent_Label"] = analysis_purpose["Percent"].apply(lambda x: f"{x:.0f}%" if x > 3 else "") # Create labels for >3% wedges to avoid overlap

            base_analysis = alt.Chart(analysis_purpose).encode(          # Setup for pie visualization
                theta=alt.Theta("Number:Q", stack=True),                 # Angle represents quantitative value of number of trips. "Q" = quantitative, should be treated as a continuous quantity
                color=alt.Color("Label:N",                               # Color mapped to nominal purpose label
                    scale=alt.Scale(scheme="tableau10"),                 # Use built-in tableau color scheme
                    legend=alt.Legend(title=None, orient="right")        # Display legend on right without title for cleaner look
                ),
                tooltip=[                                               # Setup tooltips 
                    alt.Tooltip("Label:N", title="Travel Purpose"),      
                    alt.Tooltip("Number:Q", format=",.0f"),              
                    alt.Tooltip("Percent:Q", title="Share (%)", format=".1f"), 
                ]
            )

            pie_analysis = base_analysis.mark_arc(innerRadius=0)        # Render as pie chart (inner radius 0)
            text_analysis = base_analysis.mark_text(radius=75, fontSize=12, fontWeight="bold", fill="white").encode( # Create percentage text overlay
                text=alt.Text("Percent_Label:N")                        # Map text to label column
            )

            final_analysis_pie = (pie_analysis + text_analysis).properties(height=250) # Combine chart and text, set height

            st.download_button("⬇", data=final_analysis_pie.to_html(), file_name="travel_purposes.html", mime="text/html", help="Download chart")   # Render download button
            st.markdown('<div class="section-title" style="margin-top:-6px; margin-bottom:4px;">Travel Purposes</div>', unsafe_allow_html=True)     # Render section title
            st.altair_chart(final_analysis_pie, use_container_width=True) # Render Altair chart

        budget_years = sorted([y for y in budgets["year"].dropna().unique().tolist() if y <= max_analysis_year]) # Get list of all available budget years
        
        # Calculate maximum percentage across all years to scale progress bars uniformly
        global_max_pct = 100.0                                               # Initialize minimum scale to 100%
        for budget_year in budget_years:                                     # Loop through all budget years
            temp_budget = get_budget(budgets, analysis_subunit, budget_year) # Fetch budget
           
            # If valid budget exists for this year, calculate usage percentage to determine if it sets a new maximum for scaling
            if temp_budget and temp_budget > 0:                              
                temp_used_df = df[df["year"] == budget_year].copy()          # Filter travel data for that year
                if analysis_subunit != "All":                                # Apply subunit filter
                    temp_used_df = temp_used_df[temp_used_df["subunit"] == analysis_subunit] # Filter by subunit
                temp_used = temp_used_df["CO2e RFI2.7 (t)"].sum()            # total CO2 used
                temp_pct = (temp_used / temp_budget) * 100                   # Calculate usage percentage
                if temp_pct > global_max_pct:                                # Check if this year breaks current max
                    global_max_pct = temp_pct                                # Update max value

        marker_pos = (100.0 / global_max_pct) * 100                          # Calculate position of the 100% marker line
                    
        # ─────────── BUDGET HISTORY LIST ───────────
        # Scans available historical budgets to calculate the single maximum usage.
        # This global maximum is mapped to 100% of the UI frame width to ensure 
        # bars scale uniformly and do not disrupt the CSS structure when limits are broken.

        budget_rows_html = []                                                # list to hold HTML rows
        budget_summary_rows = []                                             # list to hold table data

        for budget_year in budget_years:                                     # Loop through each budget year to gather travel data for progress bars
            year_budget = get_budget(budgets, analysis_subunit, budget_year) 
            year_used_df = df[df["year"] == budget_year].copy()              
            
            if analysis_subunit != "All":                                    # Apply subunit filter
                year_used_df = year_used_df[year_used_df["subunit"] == analysis_subunit] # Filter by subunit

            year_used = year_used_df["CO2e RFI2.7 (t)"].sum()                # Sum CO2 usage for loop year

            # Only proceed if a valid budget exists (skips missing years like 2017-2019) and prevents division by zero errors. 
            # This ensures that only years with defined budgets are visualized in the progress bars, and that the percentage calculations are meaningful and do not result 
            # in errors or misleading visualizations due to missing or zero budgets.
            if year_budget and year_budget > 0:                
                year_pct = year_used / year_budget * 100            # Calculate loop year percentage
                
                # Calculate bar width relative to global max
                year_width = (year_pct / global_max_pct) * 100      # Determine CSS width
                marker_pos = (100.0 / global_max_pct) * 100         # Keep marker consistent
                
                percent_text = format_percent(year_pct)             # Format percentage string
                status_icon, status_text = get_status(year_pct)     # Get status emoji and string
                bar_color = get_bar_color(year_pct)                 # Get bar gradient color
                
                # Generate HTML for this specific year's progress bar
                show_label = len(budget_rows_html) == 0             # Only show 100% label on the top row
                label = f"<div style='position:absolute;top:-16px;left:{marker_pos}%;transform:translateX(-50%);font-size:10px;font-weight:700;color:white;white-space:nowrap;text-shadow:0 1px 3px rgba(0,0,0,0.8);'>100%</div>" if show_label else "" # Construct conditional label HTML

                budget_rows_html.append(         # Append generated HTML to list
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

                # Store data dictionary for summary table below
                budget_summary_rows.append({                    # Add to summary list
                    "year": int(budget_year),                   # year
                    "subunit": analysis_subunit,                # subunit name
                    "co2_budget_t": year_budget,                # budget limit
                    "co2_used_t": year_used,                    # used CO2
                    "budget_used_percent": year_pct,            # percentage
                    "status": status_text,                      # status text
                })

        # Display the custom HTML progress bars if data was found
        if budget_rows_html:                                    # Check if list is populated
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
            </body></html>"""       # Build full standalone HTML document for export

            st.download_button("⬇", data=budget_html_export, file_name="co2_budget_limits.html", mime="text/html", help="Download chart") # Render download button
            st.markdown('<div class="section-title" style="margin-top:-6px; margin-bottom:4px;">CO₂ Budget Limits</div>', unsafe_allow_html=True) # Print title
            st.markdown(            # Print layout setup for HTML chart
                f"<div style='display:grid;grid-template-columns:55px 1fr 70px 34px;gap:12px;margin-bottom:2px;'>"
                f"<div></div>"
                f"<div style='position:relative;height:14px;'>"
                f"<div style='position:absolute;left:{marker_pos}%;transform:translateX(-50%);font-size:11px;font-weight:700;color:white;white-space:nowrap;text-shadow:0 1px 3px rgba(0,0,0,0.8);'>100%</div>"
                f"</div><div></div><div></div></div>",
                unsafe_allow_html=True
            )
            st.markdown("".join(budget_rows_html), unsafe_allow_html=True)                              # Render joined HTML rows
        else:                       # If no valid budget rows were generated
            st.info("No budget data available for the selected filters.")                               # Inform user

        budget_summary = pd.DataFrame(budget_summary_rows)                                              # Convert summary dictionaries to Pandas dataframe

        st.markdown('<div style="height:48px;"></div>', unsafe_allow_html=True)                         # Add vertical spacing
        st.markdown('<div class="section-title">Budget Summary Table</div>', unsafe_allow_html=True)    # Render table title

        show_budget_summary = budget_summary.copy()                                                     # Create copy for clean display formatting
        show_budget_summary["co2_budget_t"] = show_budget_summary["co2_budget_t"].map(                  # Format budget limit column
            lambda x: round(x, 1) if pd.notna(x) else None                                              # Round to 1 decimal
        )
        show_budget_summary["co2_used_t"] = show_budget_summary["co2_used_t"].map(                      # Format budget used column
            lambda x: round(x, 1) if pd.notna(x) else None                                              # Round to 1 decimal
        )
        show_budget_summary["budget_used_percent"] = show_budget_summary["budget_used_percent"].map(    # Format percentage column
            lambda x: round(x, 1) if pd.notna(x) else None                                              # Round to 1 decimal
        )

        st.dataframe(show_budget_summary, use_container_width=True, hide_index=True, key="budget_summary_table") # Render interactive Streamlit dataframe

        panel_end() # Close right analysis panel