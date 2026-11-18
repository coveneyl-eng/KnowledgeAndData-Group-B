RML Mapping Specifications And Explanations:

Prefixes:
@prefix rml: <http://semweb.mmlab.be/ns/rml#> .    --- RML Prefix
@prefix rr:  <http://www.w3.org/ns/r2rml#> .       --- R2RML Prefix - Maps Data to RDF
@prefix ql:  <http://semweb.mmlab.be/ns/ql#> .     --- RML Query Language Prefix. Specifies how to read a file (Ex:CSV)
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> . --- XML Schema for Mapping Variables
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> . --- RDFS Schema Prefix
@prefix geo:  <http://www.opengis.net/ont/geosparql#> . --- GeoSPARQL prefix for geometric mappings
@prefix dce:  <http://example.org/dce#> .          --- Our Groups ontology prefix (Data Centre Energy)



County Mapping:
county.csv
  Class:
  county_id -> dce:County
  
  Predicates:
  County rdfs:label 'name'
  County dce:inProvince Province
  rr:template "http://example.org/dce#province/{province}"

Application Mapping:
datacentre_applications_clean.csv
  Class:
  application_id -> dce: Application
  application_id -> dce: Application/Geometry
  
  Predicates:
  Application geo:hasGeometry Application/Geometry
  Application dce:decisionStatus 'decision_status'
  Application dce:applicationDate 'application_date'
  Application dce:decisionDate 'decision_date'
  Application dce:locatedIn County
  Application/Geometry geo:asWKT 'wkt' geo:wktLiteral

WindFarm Mapping:
wind_farms_clean.csv
  Class:
  WindFarm_id -> dce: WindFarm
  WindFarm_id -> dce: WindFarm/Geometry
  
  Predicates:
  WindFarm geo:hasGeometry WindFarm/Geometry
  WindFarm dce:locatedIn County
  WindFarm rdfs:label 'label'
  WindFarm dce:connection_date 'connection_date' xsd:date
  WindFarm dce:exportCapacityMW 'capacity_mw' xsd:float

FuelSource Mapping:
fuel_sources.csv
  Class:
  fuel_id -> dce: FuelSource
  
  Predicates:
  Fuel_Source rdfs:label 'fuel_name'
  Fuel_Source dce:renewable 'renewable' xsd: boolean

MEC02 Mapping:
mec02_clean.csv
  Class:
  quarter_id/sector_id -> Consumption

  Predicates:
  Consumption dce:inPeriod Quarter
  Consumption dce:value "value" xsd:float
  Consumption dce:unit 'unit' xsd:string
  Consumption dce:sector 'sector'
  
MEC03 Mapping:
mec03_clean.csv
  Class:
  year_id/county_id/sector_id -> Consumption

  Predicates:
  Consumption dce:inPeriod Year
  Consumption dce:value "value" xsd:float
  Consumption dce:unit 'unit' xsd:string
  Consumption dce:sector 'sector'
  Consumption dce:locatedIn County

MEG02 Mapping:
meg02_clean.csv
  Class:
  month_id/fuel_id -> Production

  Predicates:
  Production dce:inPeriod Month
  Production dce:value 'value' xsd:float
  Production dce:unit 'unit' xsd:string
  Production dce:hasFuelSource FuelSource

Months Mapping:
months.csv
  Class:
  month_id -> Month
  quarter_id -> Quarter
  
  Predicates:
  Month rdfs:label 'month_id'
  Month dce:inPeriod Quarter
  Quarter rdfs:label 'quarter_id'

Quarters Mapping:
quarters.csv
  Class:
  quarter_id -> Quarter
  year_id -> Year

  Predicates:
  Quarter rdfs:label 'quarter_id'
  Quarter dce:inPeriod Year
  Year rdfs:label 'year_id'

Years Mapping:
years.csv
  Class:
  year_id -> Year

  Predicates:
  Year rdfs:label 'year_id'



