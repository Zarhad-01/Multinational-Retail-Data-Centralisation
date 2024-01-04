-- Cast the columns of the orders_table to correct data types

-- Return maximum card_number length (19) 
SELECT length(cast(card_number as text)) AS card_number_length
FROM orders_table
GROUP BY card_number
ORDER BY card_number_length DESC
LIMIT 1;

-- Return maximum store code length (12)
SELECT length(cast(store_code as text)) AS store_code_length
FROM orders_table
GROUP BY store_code
ORDER BY store_code_length DESC
LIMIT 1;

-- Return maximum product code length(11)
SELECT length(cast(product_code as text)) AS product_code_length
FROM orders_table
GROUP BY product_code
ORDER BY product_code_length DESC
LIMIT 1;

-- +------------------+--------------------+--------------------+
-- |   orders_table   | current data type  | required data type |
-- +------------------+--------------------+--------------------+
-- | date_uuid        | TEXT               | UUID               |
-- | user_uuid        | TEXT               | UUID               |
-- | card_number      | TEXT               | VARCHAR(19)        |
-- | store_code       | TEXT               | VARCHAR(12)        |
-- | product_code     | TEXT               | VARCHAR(1)         |
-- | product_quantity | BIGINT             | SMALLINT           |
-- +------------------+--------------------+--------------------+

ALTER TABLE orders_table
    ALTER COLUMN date_uuid          TYPE UUID USING date_uuid::uuid,
    ALTER COLUMN user_uuid          TYPE UUID USING user_uuid::uuid,
    ALTER COLUMN card_number        TYPE VARCHAR(19),
    ALTER COLUMN store_code         TYPE VARCHAR(12),
    ALTER COLUMN product_code       TYPE VARCHAR(11),
    ALTER COLUMN product_quantity   TYPE SMALLINT;
    