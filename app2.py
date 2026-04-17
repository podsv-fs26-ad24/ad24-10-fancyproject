import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

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

    header {
        visibility: hidden;
    }

    [data-testid="stToolbar"] {
        display: none;
    }

    .stApp {
        background: linear-gradient(180deg, #062b66 0%, #032d73 100%);
        color: white;
    }

    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: white !important;
    }

    [data-testid="stSelectbox"] label, [data-testid="stMultiSelect"] label {
        color: white !important;
        font-weight: 600;
        font-size: 0.92rem !important;
    }

    [data-testid="stSelectbox"] > div > div,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: white !important;
        background-color: white !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        min-height: 40px !important;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] *,
    [data-testid="stSelectbox"] div[data-baseweb="select"] span,
    [data-testid="stSelectbox"] div[data-baseweb="select"] div,
    [data-testid="stSelectbox"] div[data-baseweb="select"] input,
    [data-testid="stSelectbox"] div[data-baseweb="select"] p {
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
    }

    [data-testid="stSelectbox"] [class*="singleValue"],
    [data-testid="stSelectbox"] [class*="SingleValue"],
    [data-testid="stSelectbox"] [class*="valueContainer"],
    [data-testid="stSelectbox"] [class*="ValueContainer"],
    [data-testid="stSelectbox"] [class*="placeholder"],
    [data-testid="stSelectbox"] [class*="Placeholder"] {
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
    }

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

    [data-testid="stDataFrame"] {
        background: transparent !important;
    }

    .metric-card {
        border-radius: 12px;
        padding: 18px 22px;
        min-height: 110px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.18);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .green-card { background: linear-gradient(135deg, #23872f, #1c7427); }
    .blue-card { background: linear-gradient(135deg, #155bb5, #104b97); }
    .gray-card { background: linear-gradient(135deg, #526684, #44576f); }
    .lightblue-card { background: linear-gradient(135deg, #2287d6, #1f72b4); }

    .metric-title {
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .metric-value {
        font-size: 27px;
        font-weight: 800;
    }

    .section-panel {
        background: rgba(255,255,255,0.015);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 14px;
        padding: 14px 16px 8px 16px;
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
        max-width: 260px;
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
# HELPERS
# =========================
@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="travel_data")
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    df["route"] = df["departure_iata"].fillna("?") + " → " + df["arrival_iata"].fillna("?")
    df["cost_CHF"] = pd.to_numeric(df["cost_CHF"], errors="coerce")
    df["CO2e RFI2.7 (t)"] = pd.to_numeric(df["CO2e RFI2.7 (t)"], errors="coerce")
    df["km"] = pd.to_numeric(df["km"], errors="coerce")
    return df

def format_chf(x: float) -> str:
    return f"{x:,.0f} CHF".replace(",", "’")

def format_tonnes(x: float) -> str:
    return f"{x:,.1f} Tonnen".replace(",", "’")

def format_int(x: float) -> str:
    return f"{int(round(x)):,}".replace(",", "’")

def format_hours(hours: float) -> str:
    if pd.isna(hours):
        return "-"
    h = int(hours)
    m = int(round((hours - h) * 60))
    if m == 60:
        h += 1
        m = 0
    return f"{h}h {m:02d}m"

def estimate_travel_time(row) -> str:
    km = row["avg_km"]
    mode = row["transport_mode"]

    if pd.isna(km):
        return "-"

    if mode == "flight":
        hours = 1.5 + (km / 800)
    elif mode == "train":
        hours = km / 120
    elif mode == "bus":
        hours = km / 80
    elif mode == "rental_car":
        hours = km / 90
    else:
        return "-"

    return format_hours(hours)

def build_metric_card(title: str, value: str, css_class: str):
    st.markdown(
        f"""
        <div class="metric-card {css_class}">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def empty_altair_theme():
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

alt.themes.register("travel_dark", empty_altair_theme)
alt.themes.enable("travel_dark")

# =========================
# LOAD DATA
# =========================
df = load_data(DATA_FILE)

# =========================
# HEADER + YEAR FILTER
# =========================
header_left, header_right = st.columns([5, 1.4])

with header_left:
    st.markdown(
        "<h1 style='text-align:left; margin-top:0.4rem; margin-bottom:0;'>Travel Insights Dashboard</h1>",
        unsafe_allow_html=True,
    )

year_values = sorted(df["year"].dropna().unique().tolist())
year_options = ["Alle"] + year_values
year_default = "Alle"

with header_right:
    st.markdown('<div class="small-filter-box">', unsafe_allow_html=True)
    st.markdown('<div class="small-filter-title">Jahr</div>', unsafe_allow_html=True)
    year = st.selectbox(
        "Jahr auswählen",
        year_options,
        index=year_options.index(year_default),
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# ROUTE OPTIONS
# =========================
all_departures = ["Alle"] + sorted(df["departure_iata"].dropna().unique().tolist())
all_arrivals = ["Alle"] + sorted(df["arrival_iata"].dropna().unique().tolist())

# =========================
# DATA SCOPES
# =========================
if year == "Alle":
    scope_df = df.copy()
else:
    scope_df = df[df["year"] == year].copy()

departure = "Alle"
arrival = "Alle"

# KPI nur nach Jahr
kpi_df = scope_df.copy()
flight_kpi_df = kpi_df[kpi_df["transport_mode"] == "flight"].copy()

# =========================
# KPI CARDS
# =========================
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    build_metric_card("Total Reisekosten", format_chf(kpi_df["cost_CHF"].sum()), "green-card")
with kpi2:
    build_metric_card("CO₂ Emissionen", format_tonnes(kpi_df["CO2e RFI2.7 (t)"].sum()), "blue-card")
with kpi3:
    build_metric_card("Anzahl Flüge", format_int(len(flight_kpi_df) if not flight_kpi_df.empty else len(kpi_df)), "gray-card")
with kpi4:
    build_metric_card("Aktuelles Jahr", str(year), "lightblue-card")

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

# =========================
# MIDDLE SECTION
# =========================
left, right = st.columns([1.05, 1], gap="large")

with left:
    st.markdown('<div class="section-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Entwicklung der Reisen</div>', unsafe_allow_html=True)

    max_display_year = max(2026, int(df["year"].max()))
    year_range = pd.DataFrame({"year": list(range(int(df["year"].min()), max_display_year + 1))})

    yearly_raw = (
        df.groupby("year", as_index=False)
        .agg(
            cost=("cost_CHF", "sum"),
            co2=("CO2e RFI2.7 (t)", "sum"),
        )
    )

    yearly = year_range.merge(yearly_raw, on="year", how="left").sort_values("year")

    cost_chart = (
        alt.Chart(yearly)
        .mark_line(point=True, strokeWidth=3, color="#65c33d")
        .encode(
            x=alt.X("year:O", title=""),
            y=alt.Y("cost:Q", title="Reisekosten (CHF)"),
            tooltip=[
                alt.Tooltip("year:O", title="Jahr"),
                alt.Tooltip("cost:Q", title="Reisekosten", format=",.0f"),
            ],
        )
        .properties(height=150)
    )

    co2_chart = (
        alt.Chart(yearly)
        .mark_line(point=True, strokeWidth=3, color="#3d7ddd")
        .encode(
            x=alt.X("year:O", title="Jahr"),
            y=alt.Y("co2:Q", title="CO₂ Emissionen (Tonnen)"),
            tooltip=[
                alt.Tooltip("year:O", title="Jahr"),
                alt.Tooltip("co2:Q", title="CO₂ (t)", format=",.1f"),
            ],
        )
        .properties(height=150)
    )

    st.altair_chart(cost_chart, use_container_width=True)
    st.altair_chart(co2_chart, use_container_width=True)

    st.markdown(
        """
        <div style="display:flex; gap:24px; padding:6px 8px 4px 8px; font-size:15px; font-weight:600;">
            <span><span style="display:inline-block;width:18px;height:10px;background:#65c33d;border-radius:3px;margin-right:8px;"></span>Reisekosten (CHF)</span>
            <span><span style="display:inline-block;width:18px;height:10px;background:#3d7ddd;border-radius:3px;margin-right:8px;"></span>CO₂ Emissionen (Tonnen)</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Travel Alternatives</div>', unsafe_allow_html=True)

    route_col1, route_col2 = st.columns(2)
    with route_col1:
        departure = st.selectbox("Abflugort auswählen", all_departures, index=all_departures.index("Alle"))
    with route_col2:
        arrival = st.selectbox("Zielort auswählen", all_arrivals, index=all_arrivals.index("Alle"))

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
        st.info("Wähle für den Alternativen-Vergleich bitte sowohl einen Abflugort als auch einen Zielort aus.")
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
        summary["sort"] = summary["transport_mode"].apply(lambda x: mode_order.index(x) if x in mode_order else 99)
        summary = summary.sort_values("sort").drop(columns="sort")

        if summary.empty:
            st.warning("Für diese Route sind keine Verkehrsmittel-Daten vorhanden.")
        else:
            summary["Option"] = summary["transport_mode"].replace(
                {
                    "flight": "Flug",
                    "train": "Zug",
                    "bus": "Bus",
                    "rental_car": "Mietwagen",
                }
            )
            summary["Reisezeit"] = summary.apply(estimate_travel_time, axis=1)
            summary["Ø Kosten"] = summary["avg_cost"].map(lambda x: format_chf(x) if pd.notna(x) else "-")
            summary["Ø CO₂ Emissionen"] = summary["avg_co2_t"].map(lambda x: f"{x*1000:.0f} kg" if pd.notna(x) else "-")
            summary["Ø Distanz"] = summary["avg_km"].map(lambda x: f"{x:,.0f} km".replace(",", "’") if pd.notna(x) else "-")

            recs = []
            min_cost = summary["avg_cost"].min() if summary["avg_cost"].notna().any() else None
            min_co2 = summary["avg_co2_t"].min() if summary["avg_co2_t"].notna().any() else None
            for _, row in summary.iterrows():
                txt = []
                if min_cost is not None and pd.notna(row["avg_cost"]) and row["avg_cost"] == min_cost:
                    txt.append("günstigste Option")
                if min_co2 is not None and pd.notna(row["avg_co2_t"]) and row["avg_co2_t"] == min_co2:
                    txt.append("umweltfreundlichste Option")
                recs.append(" & ".join(txt).capitalize() if txt else "-")
            summary["Empfehlung"] = recs

            show_df = summary[
                ["Option", "trips", "Reisezeit", "Ø Distanz", "Ø Kosten", "Ø CO₂ Emissionen", "Empfehlung"]
            ].rename(columns={"trips": "Anzahl Reisen"})
            st.dataframe(show_df, use_container_width=True, hide_index=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

# =========================
# BOTTOM SECTION
# =========================
bottom_left, bottom_right = st.columns(2, gap="large")

with bottom_left:
    st.markdown('<div class="section-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">Reisezwecke {year}</div>', unsafe_allow_html=True)

    purpose = (
        scope_df.groupby("travel_purpose", as_index=False)
        .size()
        .rename(columns={"size": "Anzahl"})
        .sort_values("Anzahl", ascending=False)
    )

    if purpose.empty:
        st.info("Keine Daten vorhanden.")
    else:
        purpose["Label"] = purpose["travel_purpose"].str.replace("_", " ").str.title()

        pie = (
            alt.Chart(purpose)
            .mark_arc(innerRadius=0)
            .encode(
                theta=alt.Theta("Anzahl:Q"),
                color=alt.Color(
                    "Label:N",
                    scale=alt.Scale(range=["#1f77d0", "#54b948", "#f7941d", "#8e5cb6", "#f1c40f", "#ff6f61"]),
                    legend=alt.Legend(title=None, orient="right"),
                ),
                tooltip=[alt.Tooltip("Label:N", title="Reisezweck"), alt.Tooltip("Anzahl:Q", format=",.0f")],
            )
            .properties(height=320)
        )
        st.altair_chart(pie, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

with bottom_right:
    st.markdown('<div class="section-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">Top Zielorte {year}</div>', unsafe_allow_html=True)

    destinations = (
        scope_df.groupby(["arrival_iata", "arrival_city"], as_index=False)
        .size()
        .rename(columns={"size": "Anzahl"})
        .sort_values("Anzahl", ascending=False)
        .head(8)
    )

    if destinations.empty:
        st.info("Keine Daten vorhanden.")
    else:
        destinations["Ziel"] = destinations.apply(
            lambda r: f"{r['arrival_iata']} – {r['arrival_city']}" if pd.notna(r["arrival_city"]) else r["arrival_iata"],
            axis=1,
        )

        bar = (
            alt.Chart(destinations)
            .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
            .encode(
                x=alt.X("Anzahl:Q", title="Anzahl Reisen"),
                y=alt.Y("Ziel:N", sort="-x", title=""),
                color=alt.Color(
                    "Ziel:N",
                    scale=alt.Scale(range=["#2d6dcc", "#4caf50", "#f57c00", "#f1c40f", "#8e44ad", "#00acc1", "#ef5350", "#9ccc65"]),
                    legend=None,
                ),
                tooltip=[alt.Tooltip("Ziel:N", title="Zielort"), alt.Tooltip("Anzahl:Q", format=",.0f")],
            )
            .properties(height=320)
        )
        st.altair_chart(bar, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

with st.expander("Rohdaten anzeigen"):
    cols_to_show = [
        "date", "transport_mode", "departure_iata", "arrival_iata",
        "departure_city", "arrival_city", "travel_purpose", "cost_CHF",
        "CO2e RFI2.7 (t)", "km", "train_alternative_available"
    ]
    existing_cols = [c for c in cols_to_show if c in scope_df.columns]
    st.dataframe(scope_df[existing_cols].sort_values("date", ascending=False), use_container_width=True, hide_index=True)