import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_excel("../data_acquisition/traveldata-export.xlsx", sheet_name="travel_data")
profile = ProfileReport(df, title="Travel Data Report",
    type_schema={
        "transport_mode": "text",
        "departure_iata": "text",
        "arrival_iata": "text",
        "arrival_city": "text",
        "arrival_country": "text",
        "arrival_continent": "text",
        "departure_city": "text",
        "departure_country": "text",
        "departure_continent": "text",
        "aircraft_type": "text",
        "business_unit": "text",
        "subunit": "text",
        "travel_purpose": "text",
        "person_type": "text",
        "haul": "text",
        "travel_class": "text",
    }
)

profile.to_file("data_report.html")
