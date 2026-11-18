# Group-C

- `http://example.org/dce#` holds the ontology (classes and properties)
- `http://example.org/dce/id/` holds the data (instances)

All data IRIs are `http://example.org/dce/id/` + one of these templates (`make_id()` creates the IDs).
county/{county_id}  
year/{year_id}  
quarter/{quarter_id}  
month/{month_id}  
fuel/{fuel_id}  
observation/mec02/{quarter_id}/{sector_id}
observation/mec03/{year_id}/{county_id}/{sector_id}
observation/meg02/{month_id}/{fuel_id}
windfarm/{windfarm_id}  
application/{application_id}

## Data Preprocessing

```bash
python preprocess.py
```

The raw data used is present under data/old_data, while the cleaned data is under data/clean_data.

### Conventions

- **IDs** are lowercase slugs, with any run of non-alphanumeric characters replaced by a hyphen (e.g. `Renewable Hydro` → `renewable-hydro`, `Co. Dublin` → `dublin`).
- **Energy values** are in **GWh** (MEG02 is converted from MWh).
- **Dates** are ISO `YYYY-MM-DD`. Periods use `YYYY`, `YYYY-Qn` and `YYYY-MM`.
- **Locations** are WGS84 longitude/latitude stored as WKT `POINT(lon lat)`, rounded to 6 decimal places.
- Rows for national totals or uncoded areas are dropped. Only the 26 counties of the Republic of Ireland are kept, plus an `offshore` pseudo-county for wind farms.

### Lookup tables (generated)

| File                                      | Description                                       |
| ----------------------------------------- | ------------------------------------------------- |
| `counties.csv`                            | 26 counties + province, plus `offshore`           |
| `years.csv`, `quarters.csv`, `months.csv` | Time hierarchy 2015–2025 (month → quarter → year) |
| `fuel_sources.csv`                        | Fuel types with a `renewable` flag                |

### Cleaned datasets

| Output                              | Source                         | Grain                  | Steps                                                                                                                                                 |
| ----------------------------------- | ------------------------------ | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mec02_clean.csv`                   | CSO MEC02                      | quarter × sector       | Electricity use by data centres vs other customers                                                                                                    |
| `mec03_clean.csv`                   | CSO MEC03                      | year × county × sector | Dublin postal districts merged into Dublin and summed                                                                                                 |
| `meg02_clean.csv`                   | CSO MEG02                      | month × fuel           | Kept "All time periods" only, dropped the all-fuels total, MWh→GWh                                                                                    |
| `datacentre_applications_clean.csv` | Irish Planning Applications    | application            | Filtered by keyword regex on the description, de-duplicated, decision standardised to Granted/Refused/Withdrawn/Invalid/Other, Web Mercator → lon/lat |
| `wind_farms_clean.csv`              | EirGrid wind farms (June 2022) | wind farm              | Irish Grid (EPSG:29903) → WGS84 via `pyproj`, offshore farms assigned `offshore`                                                                      |

## Data Proceessing

```bash
python process.py
```

Process implemnts morph_kgc to convert ttl files to triples

## Mapping/Uplifting:

RMl is used to uplift the data from CSV files into triples in RDF format. Each CSV file in clean_data has a corresponding uplifting file under `rml` folder.
The resultant triples are stored under the `Triples` folder.

## Ontology:

The ontology is defined in the `ontology_dce.ttl` file. The ontology is defined in Turtle format and the ontology graph is made using Protégé. It defines the classes and properties used in the data.

## Validate Knowledge Graph using SHACL:

Added a shapes.ttl file to validate three shapes in KG [WindFarmShape, ConsumptionShape, ProductionShape]
To validate: `curl.exe -X POST -H "Accept: text/turtle" -F "file=@<path_to_shapes.ttl_file>;type=text/turtle" "http://localhost:7200/rest/repositories/irish-data-centres-graph/validate/file"`
