import re

import numpy as np
import pandas as pd
from pyproj import Transformer


def make_id(text):
    text = str(text).lower()
    text = re.sub(
        r"[^a-z0-9]+", "-", text
    )  # Replace non-alphanumeric characters with hyphens
    return text.strip("-")


# Counties
PROVINCES = {
    "Leinster": [
        "Carlow",
        "Dublin",
        "Kildare",
        "Kilkenny",
        "Laois",
        "Longford",
        "Louth",
        "Meath",
        "Offaly",
        "Westmeath",
        "Wexford",
        "Wicklow",
    ],
    "Munster": ["Clare", "Cork", "Kerry", "Limerick", "Tipperary", "Waterford"],
    "Connacht": ["Galway", "Leitrim", "Mayo", "Roscommon", "Sligo"],
    "Ulster": ["Cavan", "Donegal", "Monaghan"],
}
counties = pd.DataFrame(
    [(make_id(c), c, p) for p, cs in PROVINCES.items() for c in cs],
    columns=["county_id", "name", "province"],
)
KNOWN = set(counties.name)

# Pseudo-county for offshore wind farms (no province); added after KNOWN so
# county_id() still treats "Offshore" as non-county for the other datasets.
counties.loc[len(counties)] = ["offshore", "Offshore", ""]

counties.to_csv("data/clean_data/counties.csv", index=False)


def county_id(raw):
    """'Co. Dublin' / 'Dublin' -> 'dublin'; anything else (Offshore, totals) -> ''."""
    name = str(raw).replace("Co. ", "").strip()
    return make_id(name) if name in KNOWN else ""


# Time periods
years = range(2015, 2026)
pd.DataFrame({"year_id": [str(y) for y in years]}).to_csv(
    "data/clean_data/years.csv", index=False
)

pd.DataFrame(
    [(f"{y}-Q{q}", str(y)) for y in years for q in range(1, 5)],
    columns=["quarter_id", "year_id"],
).to_csv("data/clean_data/quarters.csv", index=False)

pd.DataFrame(
    [(f"{y}-{m:02d}", f"{y}-Q{(m - 1) // 3 + 1}") for y in years for m in range(1, 13)],
    columns=["month_id", "quarter_id"],
).to_csv("data/clean_data/months.csv", index=False)

# Fuel sources
RENEWABLE = {
    "Wind": True,
    "Solar": True,
    "Renewable Hydro": True,
    "Other Renewable": True,
    "Biomass/Peat": False,
    "Waste": False,
    "Battery Storage": False,
    "Pumped Storage Hydro": False,
    "Coal": False,
    "Gas": False,
    "Oil": False,
    "Distillate": False,
    "Other Non-Renewable": False,
}
pd.DataFrame(
    [(make_id(f), f, str(r).lower()) for f, r in RENEWABLE.items()],
    columns=["fuel_id", "fuel_name", "renewable"],
).to_csv("data/clean_data/fuel_sources.csv", index=False)

# MEC02
mec02 = pd.read_csv(("data/old_data/MEC02.20261108132858.csv"))
SECTOR02 = {"-": "all", "10": "data-centres", "20": "other-customers"}
mec02 = pd.DataFrame(
    {
        "quarter_id": mec02["TLIST(Q1)"].str.replace("Q", "-Q"),
        "sector_id": mec02["C03907V04659"].map(SECTOR02),
        "sector": mec02["Electricity Consumption"],
        "value": mec02["VALUE"].astype(float),
        "unit": "GWh",
    }
)
mec02.to_csv("data/clean_data/mec02_clean.csv", index=False)

# MEC03
mec03 = pd.read_csv("data/old_data/MEC03.20261117100402.csv")
mec03["county_id"] = (
    mec03["Counties & Dublin Postal Districts"]
    .str.replace(r"^Dublin \d+\w*$", "Dublin", regex=True)
    .map(county_id)
)
mec03 = mec03[mec03.county_id != ""]  # drops national total and Not Coded
SECTOR03 = {"-": "all", "10": "residential", "20": "non-residential"}
mec03 = pd.DataFrame(
    {
        "year_id": mec03["Year"].astype(str),
        "county_id": mec03["county_id"],
        "sector_id": mec03["C03816V04566"].map(SECTOR03),
        "sector": mec03["Sector"].str.replace(r"^\d+ ", "", regex=True),
        "value": mec03["VALUE"].astype(float),
        "unit": "GWh",
    }
)
mec03 = mec03.groupby(
    ["year_id", "county_id", "sector_id", "sector", "unit"], as_index=False, sort=False
)["value"].sum()[["year_id", "county_id", "sector_id", "sector", "value", "unit"]]
mec03.to_csv("data/clean_data/mec03_clean.csv", index=False)

# MEG02
meg02 = pd.read_csv("data/old_data/MEG02.20261117095647.csv")
meg02 = meg02[
    (meg02["Time Bands"] == "All time periods")
    & (meg02["C04200V04972"] != "-")
    & meg02["VALUE"].notna()
]
meg02 = pd.DataFrame(
    {
        "month_id": meg02["TLIST(M1)"]
        .astype(str)
        .str.replace(r"^(\d{4})(\d{2})$", r"\1-\2", regex=True),
        "fuel_id": meg02["Primary Fuel Output"].map(make_id),
        "value": (meg02["VALUE"] / 1000).round(4),  # Convert MWh to GWh
        "unit": "GWh",
    }
)
meg02.to_csv("data/clean_data/meg02_clean.csv", index=False)

# Data centre applications
RAW_PLANNING = "data/old_data/IrishPlanningApplications_8793309899677015036.csv.gz"

DATA_CENTRE = r"\bdata[ -]?(?:centre|center|hall|storage facilit|processing (?:centre|facilit))s?\b|\bdatacent(?:re|er)|data cent$|edge computing|computing facility|hyperscale|\bserver (?:hall|building|farm)s?\b"


def planning_county(a):
    """'Fingal County Council' -> 'Dublin'; 'Cork City Council' -> 'Cork'."""
    a = (
        a.replace("Dun Laoghaire Rathdown", "Dublin")
        .replace("South Dublin", "Dublin")
        .replace("Fingal", "Dublin")
    )
    return re.sub(r"\s*(City and County|County|City) Council$", "", a)


def decision(v):
    v = str(v).strip().lower()
    if v in ("", "nan", "n/a"):
        return ""
    if "invalid" in v or "inva" in v:
        return "Invalid"
    if "withdraw" in v:
        return "Withdrawn"
    if "refus" in v:
        return "Refused"
    if "grant" in v or "conditional" in v or "approv" in v or "permission" in v:
        return "Granted"
    return "Other"


def iso_date(col):
    return pd.to_datetime(
        col, format="%m/%d/%Y %I:%M:%S %p", errors="coerce"
    ).dt.strftime("%Y-%m-%d")


app = pd.read_csv(RAW_PLANNING, low_memory=False)
description = (
    app["Development Description"]
    .fillna("")
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
)
app = app[description.str.contains(DATA_CENTRE, regex=True)].copy()
app["Application Number"] = app["Application Number"].astype(str).str.strip()

EARTH_RADIUS = 6378137.0
x = app["x"].astype(float)
y = app["y"].astype(float)
longitude = np.degrees(x / EARTH_RADIUS).round(6)
latitude = np.degrees(2 * np.arctan(np.exp(y / EARTH_RADIUS)) - np.pi / 2).round(6)

app["application_id"] = (
    app["Planning Authority"].map(make_id)
    + "-"
    + app["Application Number"].map(make_id)
)
keep = ~app.duplicated("application_id")
app, longitude, latitude = app[keep], longitude[keep], latitude[keep]
app = pd.DataFrame(
    {
        "application_id": app["application_id"],
        "label": app["Planning Authority"]
        + " "
        + app["Application Number"].astype(str),
        "county_id": app["Planning Authority"].map(planning_county).map(county_id),
        "application_date": iso_date(app["ReceivedDate"]),
        "decision_date": iso_date(app["DecisionDate"]),
        "decision_status": app["Decision"].map(decision),
        "wkt": [f"POINT({x} {y})" for x, y in zip(longitude, latitude)],
    }
)
app.to_csv("data/clean_data/datacentre_applications_clean.csv", index=False)

# Wind farms
RAW_WIND = "data/old_data/WindFarmsConnectedJune2022.csv"

wind = pd.read_csv(RAW_WIND)
irish_grid_to_wgs84 = Transformer.from_crs("EPSG:29903", "EPSG:4326", always_xy=True)
longitude, latitude = irish_grid_to_wgs84.transform(
    wind["Nat_Grid_E__substation_"].astype(float).to_numpy(),
    wind["Nat_Grid_N__substation_"].astype(float).to_numpy(),
)
name = wind["Windfarm_Name"].str.split().str.join(" ")
ref = wind["Connection_Ref"].str.strip()
date = pd.to_datetime(wind["Date_of_Connection"], format="%d/%m/%Y")

wind = pd.DataFrame(
    {
        "windfarm_id": ref.map(make_id),
        "label": name,
        "county_id": wind["County"].map(county_id).replace("", "offshore"),
        "connection_date": date.dt.strftime("%Y-%m-%d"),
        "capacity_mw": wind["MEC__MW_"],
        "wkt": [
            f"POINT({x} {y})" for x, y in zip(longitude.round(6), latitude.round(6))
        ],
    }
)
wind.to_csv("data/clean_data/wind_farms_clean.csv", index=False)
