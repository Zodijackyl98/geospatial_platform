
import pandas as pd
from sqlalchemy import create_engine
import geopandas as gpd


# Adjusting population data from a CSV, please ensure that correct file paths are used 
file_path = fr"C:\Python_Works\py\united\extras\turkey_provinces_population.csv"
    
df_raw = pd.read_csv(file_path, header=None, skiprows=6, encoding='utf-8')
    
df_raw = df_raw[df_raw[0].str.contains("Bel.", na=False)]
df_split = df_raw[0].str.split("|", expand=True)[[1, 2]]
df_split.columns = ['raw_label', 'population']


# Province = District
df_split['province_name'] = df_split['raw_label'].str.extract(r'/([^/]+ Bel\.)')
df_split = df_split[df_split['province_name'].notnull()]
    
  # veri içerisinde baş harfi büyük olacak şekilde sınıflandırılmışlar, baş harfi dönüştürme işlemi 
df_split['city_name'] = df_split['raw_label'].apply(lambda x: x.split('(')[0].strip().capitalize())
df_split['population'] = pd.to_numeric(df_split['population'], errors='coerce').fillna(0).astype(int)

# combining all municipalities of Elazig merkez into one row
filtered_df = df_split[df_split['raw_label'].str.contains("Elazığ(Merkez", na=False, regex=False)]
elazig_merkez_pop = sum(filtered_df['population'])
df_split.drop(filtered_df.index, inplace = True)

df_split.drop(columns = ['raw_label'], inplace=True)

new_row = pd.DataFrame([{'population':elazig_merkez_pop,'province_name': 'Elâzığ Merkez', 'city_name': 'Elazığ'}])
df_split = pd.concat([df_split, new_row], ignore_index=True)


df_split['province_name'] = df_split['province_name'].apply(lambda x: x.split(' ')[0])

# Elazığ and kahta sometimes written as Elazığ,Kahta sometimes as Elâzığ,Kâhta we standardize them
df_split['city_name'] = df_split['city_name'].apply(lambda x: x.replace('Elazığ', 'Elâzığ'))
df_split['province_name'] = df_split['province_name'].apply(lambda x: x.replace('Kahta','Kâhta'))
df_split['city_name'] = df_split['city_name'].apply(lambda x: x.replace('Hakkari','Hakkâri'))


df_split.to_csv(fr"C:\Python_Works\py\united\csv\turkey_provinces_population.csv", index=False)
    

engine = create_engine("postgresql://mert:password@localhost:5432/united")


# Her csv üzerinden döngü yardımıyla import işlemi
file_path = fr"C:\Python_Works\py\united\csv\turkey_provinces_population.csv"
    
# Read the file (adjust encoding if needed)
df = pd.read_csv(file_path, encoding='utf-8')
    
# Write to PostgreSQL
df.to_sql("turkey_provinces_pop", con=engine, if_exists='replace', index=False)

# sorgu, 

query = """
CREATE EXTENSION IF NOT EXISTS pg_trgm;

SELECT 
  b.name,   
  b.city_name,
  b.geometry,
  p.population
FROM turkey_provinces b
JOIN turkey_provinces_pop p
  ON b.city_name = p.city_name
 AND similarity(b.name, p.province_name) > 0.4
ORDER BY similarity(b.name, p.province_name) DESC;
"""

# Read GeoDataFrame from PostGIS
gdf = gpd.read_postgis(query, engine, geom_col="geometry")


# Reverting back to proper names
gdf['city_name'] = gdf['city_name'].apply(lambda x: x.replace('Elâzığ', 'Elazığ'))
gdf['name'] = gdf['name'].apply(lambda x: x.replace('Kâhta', 'Kahta'))
gdf['city_name'] = gdf['city_name'].apply(lambda x: x.replace('Hakkâri', 'Hakkari'))


# Save as GeoJSON
output_path = "C:/Python_Works/py/united/qgis_related/turkey_pop_matched.geojson"
gdf.to_file(output_path, driver="GeoJSON")

# Don't forget to open geojson file in qgis and then import it to your postgre database




