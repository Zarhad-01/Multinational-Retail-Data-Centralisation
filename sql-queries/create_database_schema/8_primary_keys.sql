-- Create the primary keys in the dimension tables


--Used to ensure each attribute altered is a suitable candidate for Primary key
SELECT user_uuid, COUNT(*)
FROM dim_user_table
GROUP BY user_uuid
HAVING COUNT(*) > 1 OR COUNT(user_uuid) != COUNT(*);


-- Primary Keys
ALTER TABLE dim_card_details
    ADD PRIMARY KEY (card_number);

ALTER TABLE dim_date_times
    ADD PRIMARY KEY (date_uuid);

ALTER TABLE dim_products
    ADD PRIMARY KEY (product_code);

ALTER TABLE dim_store_details
    ADD PRIMARY KEY (store_code);

ALTER TABLE dim_user_table
    ADD PRIMARY KEY (user_uuid);

ALTER TABLE orders_table
    ADD COLUMN order_id SERIAL PRIMARY KEY;