import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from sqlalchemy import create_engine

# CSV file path and table name
csv_path = r"C:\Python_Works\py\united\extras\turkey_earthy.csv"  # Change to your CSV file path
table_name = "turkey_earthy"   # Change to your desired table name

# Read CSV
df = pd.read_csv(csv_path)

# Create geometry column from longitude and latitude
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']),
    crs="EPSG:4326"
)

# Connect to PostGIS database
engine = create_engine("postgresql://mert:password@localhost:5432/united")  # Update credentials

# Export to PostGIS (geometry column will be created)
gdf.to_postgis(table_name, engine, if_exists='replace', index=False)

print(f"Table '{table_name}' with geometry column imported to PostGIS.")