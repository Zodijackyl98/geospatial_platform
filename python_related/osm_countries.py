from geoalchemy2 import Geometry
import geopandas as gpd
from sqlalchemy import create_engine
from shapely.geometry import MultiPolygon, Polygon
import json

# It's a generelazied script to update the OSM countries data in PostGIS

# Load GeoJSON, You might need to delete @relation field before reading the file
gdf = gpd.read_file(r"C:\Python_Works\py\UN\qgis_related\osm-countries-0-00001.geojson", encoding = 'utf-8')

# Create engine
engine = create_engine("postgresql://mert:password@localhost:5432/united")

def ensure_multipolygon(geom):
    if isinstance(geom, Polygon):
        return MultiPolygon([geom])
    return geom

gdf["geometry"] = gdf["geometry"].apply(ensure_multipolygon)

# save the modified GeoDataFrame back to GeoJSON
gdf.to_file(r"C:\Python_Works\py\UN\qgis_related\osm-countries-0-00001.geojson", driver="GeoJSON", encoding="utf-8")


#load the file again to ensure the geometry is in MultiPolygon format
gdf = gpd.read_file(r"C:\Python_Works\py\UN\qgis_related\osm-countries-0-00001.geojson", encoding = 'utf-8')

# Parsing 'tags' column from JSON to dictionary then creating new columns
gdf['tags'] = gdf['tags'].apply(json.loads)

gdf_columns = gdf['tags'].apply(lambda x: list(x.keys())).iloc[0]

gdf_select_col = ['name:en'] # You can add more columns to this list if needed

for i in gdf_select_col:
    gdf[i] = gdf['tags'].apply(lambda x: x[i])

# Write to PostGIS
gdf.to_postgis("osm_countries", engine, if_exists="replace", index=False, dtype={"geom": Geometry("MULTIPOLYGON", srid=4326)})
