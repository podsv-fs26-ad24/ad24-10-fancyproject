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

DATA_FILE = Path(__file__).with_name("traveldata-export.xlsx")

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
        background: linear-gradient(180deg, #062b66 0%, #032d73 100%);
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

    /* Chart / table toolbar oben rechts */
    [data-testid="stElementToolbar"] {
        background: transparent !important;
    }

    [data-testid="stElementToolbar"] button {
        background: rgba(255,255,255,0.92) !important;
        border: 1px solid rgba(0,0,0,0.15) !important;
        border-radius: 6px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.18) !important;
    }

    [data-testid="stElementToolbar"] button:hover {
        background: white !important;
    }

    [data-testid="stElementToolbar"] svg,
    [data-testid="stElementToolbar"] svg *,
    [data-testid="stElementToolbar"] path {
        color: #111827 !important;
        fill: #111827 !important;
        stroke: #111827 !important;
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
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 18px;
        padding: 24px 26px;
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
    }

    .progress-fill {
        height: 100%;
        border-radius: 10px;
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

    .cost-box {
        background: linear-gradient(135deg, #23872f, #1c7427);
        border-radius: 14px;
        padding: 18px 22px;
        margin-top: 18px;
        margin-bottom: 18px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.18);
    }

    .cost-label {
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .cost-value {
        font-size: 30px;
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
        border: 1px solid rgba(255,255,255,0.12);
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

    if selected_subunit != "Alle":
        b = b[b["subunit"] == selected_subunit]

    valid = b["co2_budget_t"].dropna()
    if valid.empty:
        return None

    return valid.sum()


def get_status(pct):
    if pct is None or pd.isna(pct):
        return "⚪", "No budget"
    if pct > 100:
        return "🔴", "Over budget"
    if pct >= 80:
        return "🟠", "Critical"
    return "🟢", "Within budget"


def get_bar_color(pct):
    if pct is None or pd.isna(pct):
        return "rgba(255,255,255,0.18)"
    if pct > 100:
        return "linear-gradient(90deg, #dc2626, #991b1b)"
    if pct >= 80:
        return "linear-gradient(90deg, #f7941d, #d97706)"
    return "linear-gradient(90deg, #3d7ddd, #245ed8)"


def altair_theme():
    return {
        "config": {
            "background": "#032d73",
            "view": {"stroke": "transparent"},
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
            "title": {"color": "white"},
        }
    }


alt.themes.register("travel_dark", altair_theme)
alt.themes.enable("travel_dark")

# =========================
# SESSION STATE
# =========================
if "dashboard_view" not in st.session_state:
    st.session_state.dashboard_view = "Boss"

# =========================
# HEADER
# =========================
header_left, header_mid, header_right = st.columns([4.5, 1.5, 1.8])

with header_left:
    st.markdown(
        "<h1 style='text-align:left; margin-top:0.4rem; margin-bottom:0;'>Travel Insights Dashboard</h1>",
        unsafe_allow_html=True,
    )

with header_mid:
    st.markdown(
        f"<div class='date-box'>Aktuelles Datum<br>{date.today().strftime('%d.%m.%Y')}</div>",
        unsafe_allow_html=True,
    )

with header_right:
    st.markdown('<div class="small-filter-box">', unsafe_allow_html=True)
    st.markdown('<div class="small-filter-title">Ansicht</div>', unsafe_allow_html=True)

    b1, b2 = st.columns(2)
    with b1:
        if st.button("Boss", use_container_width=True):
            st.session_state.dashboard_view = "Boss"
    with b2:
        if st.button("Analyse", use_container_width=True):
            st.session_state.dashboard_view = "Analyse"

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# GLOBAL OPTIONS
# =========================
current_year = 2025
max_analysis_year = 2025

year_options = ["Alle"] + sorted([y for y in df["year"].dropna().unique().tolist() if y <= max_analysis_year])
subunit_options = ["Alle"] + sorted(df["subunit"].dropna().unique().tolist())
all_departures = ["Alle"] + sorted(df["departure_iata"].dropna().unique().tolist())
all_arrivals = ["Alle"] + sorted(df["arrival_iata"].dropna().unique().tolist())

# =========================
# BOSS DASHBOARD
# =========================
if st.session_state.dashboard_view == "Boss":

    filter_col, spacer = st.columns([1.25, 4.75])

    with filter_col:
        subunit = st.selectbox("Subunit auswählen", subunit_options, index=0)

    boss_df = df[df["year"] == current_year].copy()

    if subunit != "Alle":
        boss_df = boss_df[boss_df["subunit"] == subunit]

    used_co2 = boss_df["CO2e RFI2.7 (t)"].sum()
    travel_cost = boss_df["cost_CHF"].sum()
    budget = get_budget(budgets, subunit, current_year)
    usage_pct = (used_co2 / budget * 100) if budget and budget > 0 else None
    progress_width = min(usage_pct, 100) if usage_pct is not None else 0

    left, right = st.columns([1, 1.15], gap="large")

    with left:
        panel_start(f"Subunit Overview {current_year}")

        if budget and budget > 0:
            progress_color = get_bar_color(usage_pct)

            budget_html = f"""
            <div class="budget-card">
                <div class="budget-title">CO₂ Budget</div>
                <div class="progress-bg">
                    <div class="progress-fill" style="width: {progress_width}%; background: {progress_color};"></div>
                </div>
                <div class="budget-row">
                    <div class="budget-percent">{format_percent(usage_pct)}</div>
                    <div class="budget-detail">
                        von Budget<br>
                        {format_tonnes(used_co2)} von {format_tonnes(budget)}
                    </div>
                </div>
            </div>
            """

            st.markdown(budget_html, unsafe_allow_html=True)

        else:
            st.warning("Für diese Subunit wurde im Jahr 2025 kein CO₂-Budget gefunden.")

        st.markdown(
            f"""
            <div class="cost-box">
                <div class="cost-label">Reisekosten 2025</div>
                <div class="cost-value">{format_chf(travel_cost)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="section-title">Reisezwecke</div>', unsafe_allow_html=True)

        purpose = (
            boss_df.groupby("travel_purpose", as_index=False)
            .size()
            .rename(columns={"size": "Anzahl"})
            .sort_values("Anzahl", ascending=False)
        )

        if purpose.empty:
            st.info("Keine Reisedaten für diese Auswahl vorhanden.")
        else:
            purpose["Label"] = purpose["travel_purpose"].str.replace("_", " ").str.title()

            pie = (
                alt.Chart(purpose)
                .mark_arc(innerRadius=0)
                .encode(
                    theta=alt.Theta("Anzahl:Q"),
                    color=alt.Color(
                        "Label:N",
                        scale=alt.Scale(
                            range=["#1f77d0", "#54b948", "#f7941d", "#8e5cb6", "#f1c40f", "#ff6f61"]
                        ),
                        legend=alt.Legend(title=None, orient="right"),
                    ),
                    tooltip=[
                        alt.Tooltip("Label:N", title="Reisezweck"),
                        alt.Tooltip("Anzahl:Q", format=",.0f"),
                    ],
                )
                .properties(height=290)
            )

            st.altair_chart(pie, use_container_width=True)

        panel_end()

    with right:
        panel_start("Travel Options")

        route_col1, route_col2 = st.columns(2)

        with route_col1:
            departure = st.selectbox("Abflugort auswählen", all_departures, index=0)

        with route_col2:
            arrival = st.selectbox("Zielort auswählen", all_arrivals, index=0)

        route_df = df.copy()

        if departure != "Alle":
            route_df = route_df[route_df["departure_iata"] == departure]

        if arrival != "Alle":
            route_df = route_df[route_df["arrival_iata"] == arrival]

        st.markdown(
            f"""
            <div style="margin:10px 0 12px 0; font-weight:600;">
                Datengrundlage: <span style="color:#dfe9ff;">alle Jahre</span><br>
                Route: <span style="color:#dfe9ff;">{departure if departure != "Alle" else "alle Abflugorte"} → {arrival if arrival != "Alle" else "alle Zielorte"}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if departure == "Alle" or arrival == "Alle":
            st.info("Wähle bitte Abflugort und Zielort aus.")
        elif route_df.empty:
            st.warning("Für diese Route gibt es keine Daten.")
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
                    "flight": "Flug",
                    "train": "Zug",
                    "bus": "Bus",
                    "rental_car": "Mietwagen",
                }
            )

            summary["Ø Kosten"] = summary["avg_cost"].map(lambda x: format_chf(x) if pd.notna(x) else "-")
            summary["Ø CO₂"] = summary["avg_co2_t"].map(lambda x: f"{x*1000:.0f} kg" if pd.notna(x) else "-")
            summary["Ø Distanz"] = summary["avg_km"].map(lambda x: f"{x:,.0f} km".replace(",", "’") if pd.notna(x) else "-")

            min_cost = summary["avg_cost"].min()
            min_co2 = summary["avg_co2_t"].min()

            def recommendation(row):
                tags = []
                if row["avg_cost"] == min_cost:
                    tags.append("günstigste Option")
                if row["avg_co2_t"] == min_co2:
                    tags.append("umweltfreundlichste Option")
                return " & ".join(tags).capitalize() if tags else "-"

            summary["Empfehlung"] = summary.apply(recommendation, axis=1)

            show_df = summary[
                ["Option", "trips", "Ø Distanz", "Ø Kosten", "Ø CO₂", "Empfehlung"]
            ].rename(columns={"trips": "Anzahl Reisen"})

            st.dataframe(show_df, use_container_width=True, hide_index=True)

        panel_end()

# =========================
# ANALYSE DASHBOARD
# =========================
else:
    filter_col1, filter_col2, spacer = st.columns([1.2, 1.4, 3.4])

    with filter_col1:
        analysis_year = st.selectbox("Jahr auswählen", year_options, index=0)

    with filter_col2:
        analysis_subunit = st.selectbox("Subunit auswählen", subunit_options, index=0)

    analysis_df = df[df["year"] <= max_analysis_year].copy()

    if analysis_year != "Alle":
        analysis_df = analysis_df[analysis_df["year"] == analysis_year]

    if analysis_subunit != "Alle":
        analysis_df = analysis_df[analysis_df["subunit"] == analysis_subunit]

    left, right = st.columns([1.15, 1], gap="large")

    with left:
        panel_start("CO₂ Analyse")

        cumulative_df = df[df["year"] <= max_analysis_year].copy()

        if analysis_subunit != "Alle":
            cumulative_df = cumulative_df[cumulative_df["subunit"] == analysis_subunit]

        yearly_co2 = (
            cumulative_df.groupby("year", as_index=False)
            .agg(yearly_co2=("CO2e RFI2.7 (t)", "sum"))
            .sort_values("year")
        )

        if yearly_co2.empty:
            st.info("Keine CO₂-Daten für den kumulierten Zeitverlauf vorhanden.")
        else:
            all_years = pd.DataFrame(
                {"year": list(range(int(df["year"].min()), max_analysis_year + 1))}
            )

            yearly_co2 = all_years.merge(yearly_co2, on="year", how="left")
            yearly_co2["yearly_co2"] = yearly_co2["yearly_co2"].fillna(0)
            yearly_co2["cumulative_co2"] = yearly_co2["yearly_co2"].cumsum()

            cumulative_chart = (
                alt.Chart(yearly_co2)
                .mark_line(point=True, strokeWidth=3, color="#3d7ddd")
                .encode(
                    x=alt.X("year:O", title="Jahr"),
                    y=alt.Y("cumulative_co2:Q", title="Kumulierte CO₂-Emissionen (t)"),
                    tooltip=[
                        alt.Tooltip("year:O", title="Jahr"),
                        alt.Tooltip("yearly_co2:Q", title="CO₂ im Jahr (t)", format=",.1f"),
                        alt.Tooltip("cumulative_co2:Q", title="CO₂ kumuliert (t)", format=",.1f"),
                    ],
                )
                .properties(
                    title=f"Kumulierte CO₂-Emissionen über die Jahre – {analysis_subunit}",
                    height=300,
                )
            )

            st.altair_chart(cumulative_chart, use_container_width=True)

        st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)

        if analysis_year == "Alle":
            line_year = current_year
        else:
            line_year = int(analysis_year)

        line_df = df[(df["year"] == line_year) & (df["year"] <= max_analysis_year)].copy()

        if analysis_subunit != "Alle":
            line_df = line_df[line_df["subunit"] == analysis_subunit]

        line_df = (
            line_df.groupby("month", as_index=False)
            .agg(monthly_co2=("CO2e RFI2.7 (t)", "sum"))
            .sort_values("month")
        )

        if line_df.empty:
            st.info("Keine Daten für den Jahresverlauf vorhanden.")
        else:
            all_months = pd.DataFrame(
                {
                    "month": pd.date_range(
                        start=f"{line_year}-01-01",
                        end=f"{line_year}-12-01",
                        freq="MS",
                    )
                }
            )

            line_df = all_months.merge(line_df, on="month", how="left")
            line_df["monthly_co2"] = line_df["monthly_co2"].fillna(0)
            line_df["cumulative_co2"] = line_df["monthly_co2"].cumsum()

            line_budget = get_budget(budgets, analysis_subunit, line_year)

            co2_line = (
                alt.Chart(line_df)
                .mark_line(point=True, strokeWidth=3, color="#f7941d")
                .encode(
                    x=alt.X("month:T", title="Monat"),
                    y=alt.Y("cumulative_co2:Q", title="Kumulierte CO₂-Emissionen (t)"),
                    tooltip=[
                        alt.Tooltip("month:T", title="Monat", format="%b %Y"),
                        alt.Tooltip("monthly_co2:Q", title="CO₂ im Monat (t)", format=",.1f"),
                        alt.Tooltip("cumulative_co2:Q", title="CO₂ kumuliert (t)", format=",.1f"),
                    ],
                )
            )

            if line_budget and line_budget > 0:
                budget_rule_data = pd.DataFrame({"budget": [line_budget]})

                budget_rule = (
                    alt.Chart(budget_rule_data)
                    .mark_rule(color="#dc2626", strokeWidth=3, strokeDash=[6, 4])
                    .encode(
                        y="budget:Q",
                        tooltip=[
                            alt.Tooltip("budget:Q", title="Budgetlimit (t)", format=",.1f")
                        ],
                    )
                )

                line_chart = (
                    (co2_line + budget_rule)
                    .properties(
                        title=f"Kumulierte CO₂-Emissionen {line_year} mit Budgetlimit",
                        height=330,
                    )
                )
            else:
                line_chart = (
                    co2_line
                    .properties(
                        title=f"Kumulierte CO₂-Emissionen {line_year}",
                        height=330,
                    )
                )

            st.altair_chart(line_chart, use_container_width=True)

        panel_end()

    with right:
        panel_start("Analyse Summary")

        context_year = "Alle Jahre" if analysis_year == "Alle" else str(analysis_year)
        context_subunit = analysis_subunit

        st.markdown(
            f"""
            <div class="analysis-context">
                Analyse: <span style="color:#dfe9ff;">{context_year}</span> |
                Subunit: <span style="color:#dfe9ff;">{context_subunit}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        total_trips = len(analysis_df)
        flight_count = len(analysis_df[analysis_df["transport_mode"] == "flight"])
        train_count = len(analysis_df[analysis_df["transport_mode"] == "train"])
        bus_count = len(analysis_df[analysis_df["transport_mode"] == "bus"])
        car_count = len(analysis_df[analysis_df["transport_mode"] == "rental_car"])

        st.markdown(
            f"""
            <div class="analysis-metric-grid">
                <div class="analysis-metric-card">
                    <div class="analysis-metric-label">Anzahl Reisen</div>
                    <div class="analysis-metric-value">{format_int(total_trips)}</div>
                </div>
                <div class="analysis-metric-card">
                    <div class="analysis-metric-label">Anzahl Flüge</div>
                    <div class="analysis-metric-value">{format_int(flight_count)}</div>
                </div>
                <div class="analysis-metric-card">
                    <div class="analysis-metric-label">Anzahl Zug</div>
                    <div class="analysis-metric-value">{format_int(train_count)}</div>
                </div>
                <div class="analysis-metric-card">
                    <div class="analysis-metric-label">Anzahl Bus</div>
                    <div class="analysis-metric-value">{format_int(bus_count)}</div>
                </div>
                <div class="analysis-metric-card">
                    <div class="analysis-metric-label">Anzahl Mietwagen</div>
                    <div class="analysis-metric-value">{format_int(car_count)}</div>
                </div>
                <div class="analysis-metric-card">
                    <div class="analysis-metric-label">CO₂ Emissionen</div>
                    <div class="analysis-metric-value">{format_tonnes(analysis_df["CO2e RFI2.7 (t)"].sum())}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="section-title">Reisezwecke</div>', unsafe_allow_html=True)

        analysis_purpose = (
            analysis_df.groupby("travel_purpose", as_index=False)
            .size()
            .rename(columns={"size": "Anzahl"})
            .sort_values("Anzahl", ascending=False)
        )

        if analysis_purpose.empty:
            st.info("Keine Reisedaten für diese Auswahl vorhanden.")
        else:
            analysis_purpose["Label"] = analysis_purpose["travel_purpose"].str.replace("_", " ").str.title()

            analysis_pie = (
                alt.Chart(analysis_purpose)
                .mark_arc(innerRadius=0)
                .encode(
                    theta=alt.Theta("Anzahl:Q"),
                    color=alt.Color(
                        "Label:N",
                        scale=alt.Scale(
                            range=["#1f77d0", "#54b948", "#f7941d", "#8e5cb6", "#f1c40f", "#ff6f61"]
                        ),
                        legend=alt.Legend(title=None, orient="right"),
                    ),
                    tooltip=[
                        alt.Tooltip("Label:N", title="Reisezweck"),
                        alt.Tooltip("Anzahl:Q", format=",.0f"),
                    ],
                )
                .properties(height=250)
            )

            st.altair_chart(analysis_pie, use_container_width=True)

        st.markdown('<div class="section-title">CO₂ Budgetlimits</div>', unsafe_allow_html=True)

        budget_years = sorted([y for y in budgets["year"].dropna().unique().tolist() if y <= max_analysis_year])
        budget_rows_html = []
        budget_summary_rows = []

        for budget_year in budget_years:
            year_budget = get_budget(budgets, analysis_subunit, budget_year)

            year_used_df = df[df["year"] == budget_year].copy()
            if analysis_subunit != "Alle":
                year_used_df = year_used_df[year_used_df["subunit"] == analysis_subunit]

            year_used = year_used_df["CO2e RFI2.7 (t)"].sum()

            if year_budget and year_budget > 0:
                year_pct = year_used / year_budget * 100
                year_width = min(year_pct, 100)
                percent_text = format_percent(year_pct)
                status_icon, status_text = get_status(year_pct)
                bar_color = get_bar_color(year_pct)
            else:
                year_pct = None
                year_width = 0
                percent_text = "-"
                status_icon, status_text = "⚪", "No budget"
                bar_color = "rgba(255,255,255,0.18)"

            budget_rows_html.append(
                f"""
                <div class="budget-history-row">
                    <div class="budget-history-year">{int(budget_year)}</div>
                    <div class="budget-history-bg">
                        <div class="budget-history-fill" style="width:{year_width}%; background:{bar_color};"></div>
                    </div>
                    <div class="budget-history-percent">{percent_text}</div>
                    <div class="budget-status" title="{status_text}">{status_icon}</div>
                </div>
                """
            )

            budget_summary_rows.append(
                {
                    "year": int(budget_year),
                    "subunit": analysis_subunit,
                    "co2_budget_t": year_budget,
                    "co2_used_t": year_used,
                    "budget_used_percent": year_pct,
                    "status": status_text,
                }
            )

        st.markdown("".join(budget_rows_html), unsafe_allow_html=True)

        budget_summary = pd.DataFrame(budget_summary_rows)

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

        st.dataframe(show_budget_summary, use_container_width=True, hide_index=True)

        panel_end()