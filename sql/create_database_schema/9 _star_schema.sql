-- Finalising the star-based schema & adding the foreign keys to the orders table.

-- Find card numbers in orders_table not present in dim_card_details
SELECT card_number
FROM orders_table ot
WHERE NOT EXISTS (
    SELECT 1
    FROM dim_card_details dcd
    WHERE ot.card_number = dcd.card_number
);

-- Insert missing card numbers into dim_card_details
INSERT INTO dim_card_details (card_number)
SELECT DISTINCT card_number
FROM orders_table
WHERE card_number NOT IN (
    SELECT card_number
    FROM dim_card_details
);

-- Repeat similar steps for user_uuid, store_code, and product_code

-- Find user_uuids not present in dim_users
SELECT user_uuid
FROM orders_table ot
WHERE NOT EXISTS (
    SELECT 1
    FROM dim_user_table du
    WHERE ot.user_uuid = du.user_uuid
);

-- Insert missing user_uuids into dim_user_table
INSERT INTO dim_user_table (user_uuid)
SELECT DISTINCT user_uuid
FROM orders_table
WHERE user_uuid NOT IN (
    SELECT user_uuid
    FROM dim_user_table
);

-- Find store_codes not present in dim_store_details
SELECT store_code
FROM orders_table ot
WHERE NOT EXISTS (
    SELECT 1
    FROM dim_store_details dsd
    WHERE ot.store_code = dsd.store_code
);

-- Insert missing store_codes into dim_store_details
INSERT INTO dim_store_details (store_code)
SELECT DISTINCT store_code
FROM orders_table
WHERE store_code NOT IN (
    SELECT store_code
    FROM dim_store_details
);

-- Find product_codes not present in dim_products
SELECT product_code
FROM orders_table ot
WHERE NOT EXISTS (
    SELECT 1
    FROM dim_products dp
    WHERE ot.product_code = dp.product_code
);

-- Insert missing product_codes into dim_products
INSERT INTO dim_products (product_code)
SELECT DISTINCT product_code
FROM orders_table
WHERE product_code NOT IN (
    SELECT product_code
    FROM dim_products
);

-- Adding foreign keys
ALTER TABLE orders_table
ADD FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid);

ALTER TABLE orders_table
ADD FOREIGN KEY (user_uuid) REFERENCES dim_user_table(user_uuid);

ALTER TABLE orders_table
ADD FOREIGN KEY (card_number) REFERENCES dim_card_details(card_number);

ALTER TABLE orders_table
ADD FOREIGN KEY (store_code) REFERENCES dim_store_details(store_code);

ALTER TABLE orders_table
ADD FOREIGN KEY (product_code) REFERENCES dim_products(product_code);
