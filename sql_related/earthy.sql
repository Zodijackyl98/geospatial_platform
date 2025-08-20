ALTER TABLE turkey_earthy
ADD COLUMN city_name TEXT;

UPDATE turkey_earthy p
SET city_name = c.name
FROM turkey_cities c
WHERE ST_Contains(c.geometry, p.geometry);

ALTER TABLE turkey_earthy
ADD COLUMN province_name TEXT;

UPDATE turkey_earthy p
SET province_name = c.name
FROM turkey_provinces c
WHERE ST_Contains(c.geometry, p.geometry);

-- Add the province_name column if not already present
ALTER TABLE turkey_earthy
ADD COLUMN IF NOT EXISTS province_name_near TEXT;

-- Update each point with the name of the nearest province
UPDATE turkey_earthy p
SET province_name_near = sub.name
FROM (
    SELECT p.id, c.name
    FROM turkey_earthy p
    JOIN LATERAL (
        SELECT name
        FROM turkey_provinces c
        ORDER BY c.geometry <-> p.geometry
        LIMIT 1
    ) c ON true
) sub
WHERE p.id = sub.id;

-- Assigning country names with respect to osm boundaries
ALTER TABLE turkey_earthy
ADD COLUMN country_name TEXT;

UPDATE turkey_earthy n
SET country_name = c."name:en"
FROM  osm_countries c
WHERE ST_Contains(c.geometry, n.geometry);