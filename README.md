# United Geospatial Data Platform
The workflow integrates Python (Pandas, SQLAlchemy, GeoPandas) and PostgreSQL/PostGIS for data management and spatial operations. This repository provides tools and scripts for processing, enriching, and analyzing geospatial datasets related to mostly Turkey for now but also including administrative boundaries of countries.

## Features
   -  Automated Data Import: Scripts to import CSV and GeoJSON data into PostgreSQL/PostGIS.
   -  Spatial Joins: SQL scripts to assign city, province, and country names to geometries using spatial joins.
   -  QGIS Compatibility: Outputs and intermediate files are compatible with QGIS for further spatial analysis and visualization.
   -  Showing examples For Population Data & Sentinel Satellite Data Integration: Includes georeferenced raster and vector data for advanced analysis.

## Folder Structure
   -  csv/: Cleaned and processed CSV files, e.g., province population data.
   -  extras/: GeoJSON files for Turkish administrative boundaries and neighbourhoods also contains USGS Earthquake data across Turkey.
   -  python_related/: Python scripts for different needs, detailed explanations can be found in the scripts.
   -  qgis_related/: QGIS project files and additional spatial datasets.
   -  sql_related/: SQL scripts for creating and updating spatial tables.
   
## Workflow Overview

### 1. Data Preparation
Place raw and cleaned CSV/GeoJSON files in the appropriate folders (csv/, extras/). Due to limitation of large files that exceeds 100Mb, I could not upload some of the major GeoJSON files such as all neighbourhoods in Turkey via OpenStreetMap and all country boundaries(visit: https://github.com/Zaczero/osm-countries-geojson). All other GeoJSON files
were collected using Overpass Turbo(https://overpass-turbo.eu/). Some script examples will be added in the future updates.  

### 2. Import Data to PostgreSQL/PostGIS
Use `python_related/to_postgre.py` to import GeoJSON and CSV data into the database.
Use `update_provinces.py` to clean and match population data, then upload to PostgreSQL.
Use `osm_countries.py` to transform the polygon to multipolygon and then parse the tags column to create new columns before importing dataframe into your database.
Explanation for the rest of the scripts can be found within themselves.
### 3. Spatial Enrichment
Run `creating_geometries.sql` to:
Add city and province names to spatial tables using spatial joins.
Assign country names using OSM boundaries.
Calculate area for each province.
Use `earthy.sql` for further enrichment, such as assigning nearest province names and country overlays to point datasets.

### 4. Analysis & Visualization
Use QGIS with files in qgis_related/ for spatial analysis and visualization.
Sentinel satellite data and processed rasters are available for advanced geospatial analysis.
Cleaning province and city names for consistency.
Exporting the cleaned data to CSV.
Importing the data into PostgreSQL.
Running a SQL query to join spatial boundaries with population data using fuzzy matching.

## Requirements
Python 3.x,
PostgreSQL with PostGIS extension
Python packages: pandas, sqlalchemy, geopandas, psycopg2

## Usage
Install dependencies:

pip install pandas sqlalchemy geopandas psycopg2
Set up PostgreSQL/PostGIS database, it's set to localhost and a username in the scripts.
Execute the SQL scripts in `sql_related/` in your PostgreSQL database block by block starting with `creating_geometries.sql`.
Run the Python scripts in `python_related/` as needed.
Open QGIS project files for visualization and further analysis.

## Notes
Ensure your database connection parameters are set correctly in the Python scripts.
Some scripts require the pg_trgm extension for fuzzy string matching in SQL.
GeoJSON and raster files are provided for QGIS and advanced spatial analysis.

## Example Use Cases
Will be added shortly
