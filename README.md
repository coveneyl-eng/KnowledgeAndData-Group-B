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
