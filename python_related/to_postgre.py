from geoalchemy2 import Geometry
import geopandas as gpd
from sqlalchemy import create_engine
from shapely.geometry import MultiPolygon, Polygon

# Load GeoJSON, You need to delete @relation field before reading the file
# This script can be used to integrate any geojson file into postgis with multipolygon support
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

