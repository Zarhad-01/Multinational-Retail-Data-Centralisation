-- Update the dim_date_times table

-- +-----------------+-------------------+--------------------+
-- | dim_date_times  | current data type | required data type |
-- +-----------------+-------------------+--------------------+
-- | month           | TEXT              | VARCHAR(2)         |
-- | year            | TEXT              | VARCHAR(4)         |
-- | day             | TEXT              | VARCHAR(2)         |
-- | time_period     | TEXT              | VARCHAR(10)        |
-- | date_uuid       | TEXT              | UUID               |
-- +-----------------+-------------------+--------------------+

ALTER TABLE dim_date_times
    ALTER COLUMN month          TYPE VARCHAR(2),
    ALTER COLUMN year           TYPE VARCHAR(4),
    ALTER COLUMN day            TYPE VARCHAR(2),
    ALTER COLUMN time_period    TYPE VARCHAR(10),
    ALTER COLUMN date_uuid      TYPE UUID using date_uuid::uuid;
