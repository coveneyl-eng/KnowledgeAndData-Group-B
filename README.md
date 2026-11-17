# KnowledgeAndData-Group-9

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

## Data Used:

The raw data used is present under data/old_data, while the cleaned data is under data/clean_data.
`preprocess.py` cleans the data, extracts relevant columns and stores it under clean_data.

## Mapping/Uplifting:

RMl is used to uplift the data from CSV files into triples in RDF format. Each CSV file in clean_data has a corresponding uplifting file under `rml` folder.
The resultant triples are stored under the `Triples` folder.

## Ontology:

The ontology is defined in the `ontology_dce.ttl` file. The ontology is defined in Turtle format and the ontology graph is made using Protégé. It defines the classes and properties used in the data.

## Validate Knowledge Graph using SHACL:

Added a shapes.ttl file to validate three shapes in KG [WindFarmShape, ConsumptionShape, ProductionShape]
To validate: `curl.exe -X POST -H "Accept: text/turtle" -F "file=@<path_to_shapes.ttl_file>;type=text/turtle" "http://localhost:7200/rest/repositories/irish-data-centres-graph/validate/file"`

## SPARQL Queries

1. **Granted applications by county:** Which counties have the most granted data-centre planning applications?
2. **Quarterly data-centre consumption:** How much electricity did data centres consume in each quarter?
3. **Applications and wind capacity by county:** Are data-centre applications in the same counties as wind capacity?
4. **Nearest wind farm:** How far is each granted data-centre application from the nearest wind farm?
5. **Wind vs data-centre consumption:** How does national wind generation compare with data-centre consumption each quarter?
6. **Share of renewable generation:** What share of renewable generation would data-centre consumption use each year?
7. **Below-average counties:** Which counties with data-centre applications have below-average non-residential electricity consumption, and what was decided on those applications?
