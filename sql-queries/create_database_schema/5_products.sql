-- Update the dim_products table with the required data types
--

ALTER TABLE dim_products
    RENAME COLUMN removed TO still_available;

UPDATE dim_products
SET still_available = CASE
    WHEN TRIM(still_available) = 'Removed' THEN FALSE
    ELSE TRUE
END;

ALTER TABLE dim_products
    ALTER COLUMN product_price TYPE FLOAT USING CAST(product_price AS FLOAT),
    ALTER COLUMN weight TYPE FLOAT USING CAST(weight AS FLOAT),
    ALTER COLUMN "EAN" TYPE VARCHAR(13),
    ALTER COLUMN product_code TYPE VARCHAR(11),
    ALTER COLUMN date_added TYPE DATE,
    ALTER COLUMN uuid TYPE UUID USING uuid::uuid,
	ALTER COLUMN still_available TYPE BOOL USING still_available::boolean,
    ALTER COLUMN weight_class TYPE VARCHAR(14);
