-- Cast the columns of the dim_users_table to the correct data types

-- Used to find the max length of country_code (2)
SELECT length(cast(country_code as text)) AS country_code_length
FROM dim_user_table
GROUP BY country_code
ORDER BY country_code_length DESC
LIMIT 1;

-- +----------------+--------------------+--------------------+
-- | dim_user_table | current data type  | required data type |
-- +----------------+--------------------+--------------------+
-- | first_name     | TEXT               | VARCHAR(255)       |
-- | last_name      | TEXT               | VARCHAR(255)       |
-- | date_of_birth  | TEXT               | DATE               |
-- | country_code   | TEXT               | VARCHAR(2)         |
-- | user_uuid      | TEXT               | UUID               |
-- | join_date      | TEXT               | DATE               |
-- +----------------+--------------------+--------------------+

ALTER TABLE dim_user_table
    ALTER COLUMN first_name     TYPE VARCHAR(255),
    ALTER COLUMN last_name      TYPE VARCHAR(255),
    ALTER COLUMN date_of_birth  TYPE DATE,
    ALTER COLUMN country_code   TYPE VARCHAR(2),
    ALTER COLUMN user_uuid      TYPE UUID USING user_uuid::uuid,
    ALTER COLUMN join_date      TYPE DATE