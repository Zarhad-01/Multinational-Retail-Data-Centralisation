-- Update dim_store_details table.

-- Used to confirm max length of the country_code (2)
SELECT length(cast(country_code as text)) AS country_code_length
FROM dim_store_details
GROUP BY country_code
ORDER BY country_code_length DESC
LIMIT 1;

-- Used to confirm max length of the store_code (12)
SELECT length(cast(store_code as text)) AS store_code_length
FROM dim_store_details
GROUP BY store_code
ORDER BY store_code_length DESC
LIMIT 1;

-- +---------------------+-------------------+------------------------+
-- | store_details_table | current data type |   required data type   |
-- +---------------------+-------------------+------------------------+
-- | longitude           | TEXT              | FLOAT                  |
-- | locality            | TEXT              | VARCHAR(255)           |
-- | store_code          | TEXT              | VARCHAR(12)            |
-- | staff_numbers       | TEXT              | SMALLINT               |
-- | opening_date        | TEXT              | DATE                   |
-- | store_type          | TEXT              | VARCHAR(255) NULLABLE  |
-- | latitude            | TEXT              | FLOAT                  |
-- | country_code        | TEXT              | VARCHAR(2)             |
-- | continent           | TEXT              | VARCHAR(255)           |
-- +---------------------+-------------------+------------------------+

ALTER TABLE dim_store_details
    ALTER COLUMN longitude      TYPE FLOAT USING CAST(longitude AS FLOAT),
    ALTER COLUMN locality       TYPE VARCHAR(255),
    ALTER COLUMN store_code     TYPE VARCHAR(12),
    ALTER COLUMN staff_numbers  TYPE SMALLINT,
    ALTER COLUMN opening_date   TYPE DATE USING CAST(opening_date AS DATE),
    ALTER COLUMN store_type     TYPE VARCHAR(255),
    ALTER COLUMN latitude       TYPE FLOAT USING CAST(latitude AS FLOAT),
    ALTER COLUMN country_code   TYPE VARCHAR(2),
    ALTER COLUMN continent      TYPE VARCHAR(255);