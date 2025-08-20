CREATE EXTENSION IF NOT EXISTS postgis;

-- Creating tables before assinging the geom fields, run them before running the python script

CREATE TABLE istanbul_provinces (
    id SERIAL PRIMARY KEY,
    name TEXT,
    geom GEOMETRY(MULTIPOLYGON, 4326)  -- Geometry column for polygons
);

CREATE TABLE turkey_cities (
    id SERIAL PRIMARY KEY,
    name TEXT,
    geom GEOMETRY(MULTIPOLYGON, 4326)  -- Geometry column for polygons
);

CREATE TABLE turkey_provinces (
    id SERIAL PRIMARY KEY,
    name TEXT,
    geom GEOMETRY(MULTIPOLYGON, 4326)  -- Geometry column for polygons
);

CREATE TABLE turkey_neighbourhood (
    id SERIAL PRIMARY KEY,
    name TEXT,
    geom GEOMETRY(MULTIPOLYGON, 4326)  -- Geometry column for polygons
);


-- For all provinces of Turkey

ALTER TABLE turkey_provinces
ADD COLUMN city_name TEXT;

UPDATE turkey_provinces t
SET city_name = c.name
FROM turkey_cities c
WHERE ST_Contains(c.geometry, t.geometry);


-- For all neighbourhoods 
ALTER TABLE turkey_neighbourhood
ADD COLUMN city_name TEXT;

UPDATE turkey_neighbourhood n
SET city_name = c.city_name
FROM turkey_provinces c
WHERE ST_Contains(c.geometry, n.geometry);

ALTER TABLE turkey_neighbourhood
ADD COLUMN province_name TEXT;

UPDATE turkey_neighbourhood n
SET province_name = c.name
FROM turkey_provinces c
WHERE ST_Contains(c.geometry, n.geometry);

-- Don't forget to change name to hood_name in turkey_all_neighbourhood
ALTER TABLE turkey_neighbourhood RENAME COLUMN name TO hood_name;

-- Assigning country names into turkey_provinces
ALTER TABLE turkey_provinces
ADD COLUMN country_name TEXT;

UPDATE turkey_provinces n
SET country_name = c."name:en"
FROM  osm_countries c
WHERE ST_Contains(c.geometry, n.geometry);

-- Calculate area of every provinces in Turkey
ALTER TABLE turkey_provinces ADD COLUMN area_km2 NUMERIC;

UPDATE turkey_provinces
SET area_km2 = ROUND((ST_Area(geometry::geography) / 1000000)::NUMERIC, 4);

-- Calculate area of every city in Turkey
ALTER TABLE turkey_cities ADD COLUMN area_km2 NUMERIC;

UPDATE turkey_cities
SET area_km2 = ROUND((ST_Area(geometry::geography) / 1000000)::NUMERIC, 4);

-- Below codes are meant to run only if you have polygons that were transformed from rasters
-- Calculate Area of Urban buildings in Kadikoy
SELECT SUM(ST_Area(ST_Transform(geom, 32635))) / 1000000 AS total_area_km2
FROM sentinel_urban_filtered;

-- Calculate Vegetation in Kadikoy
SELECT SUM(ST_Area(ST_Transform(geom, 32635))) / 1000000 AS total_area_km2
FROM sentinel_vegetation_custom 

-- Calculate Vegetation in Kadikoy
SELECT SUM(ST_Area(ST_Transform(geom, 32635))) / 1000000 AS total_area_km2
FROM sentinel_vegetation_atasehir 

-- Create a column and then calculate Vegetation of every geometry in Atasehir
ALTER TABLE sentinel_vegetation_atasehir ADD COLUMN veg_area NUMERIC;
UPDATE sentinel_vegetation_atasehir SET veg_area = ST_Area(ST_Transform(geom, 32635)) / 1000000;


