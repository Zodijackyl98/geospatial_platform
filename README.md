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
### Population Data
<img width="1920" height="1357" alt="ankara_district_pop" src="https://github.com/Zodijackyl98/geospatial_platform/blob/main/qgis_related/examples/ankara_district_pop.png" />

### Earthquake Data
Earthquakes mag >= 3.0  that occured in Turkey according to USGS.
<img width="1920" height="1357" alt="turkey_earthy_ex" src="https://github.com/Zodijackyl98/geospatial_platform/blob/main/qgis_related/examples/turkey_earthy_ex.png" />

Earthqakes that have episentr located outside of lands but still resides in Turkey. This was achieved only applying filters to the corresponding table, no area selection tool was used. Information can be found inside `earthy.sql`.
<img width="1920" height="1357" alt="turkey_earthy_sea_only" src="https://github.com/Zodijackyl98/geospatial_platform/blob/main/qgis_related/examples/turkey_earthy_sea_only.png" />

### Satellite Data
Using Sentinel Hub services and applying two different custom scripts for detection of respectively urban building and vegetation detection for a particular district in Istanbul.
Total area of vegetation can be calculated by applying making simple queries in `create_geometries.sql`.
Total calculated area of Kadıköy district is 25.13 km2 and about %42 of the total area counts as vegetation according to the calculations. If we take Ataşehir which is another district that is adjacent to Kadıköy that also shares similar total area of 25.22 km2, total calculated vegetation of that distict is 7.59 km2 which equals about %30 of the total area. To conclude, even though Kadıköy and Ataşehir districts share similar total area, Kadıköy is %12 greener than Ataşehir. 
<img width="1920" height="1357" alt="urban_building_kadikoy" src="https://github.com/Zodijackyl98/geospatial_platform/blob/main/qgis_related/examples/urban_building_kadikoy.png" />


<img width="1920" height="1357" alt="vegetation_kadikoy" src="https://github.com/Zodijackyl98/geospatial_platform/blob/main/qgis_related/examples/vegetation_kadikoy.png" />

<img width="1920" height="1357" alt="vegetation_atasehir" src="https://github.com/Zodijackyl98/geospatial_platform/blob/main/qgis_related/examples/vegetation_atasehir.png" />


