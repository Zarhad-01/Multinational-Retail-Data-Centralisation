-- Query to calculate the number and quantity of products sold online and offline
-- Online Sales
SELECT
    COUNT(*) AS number_of_sales,
    SUM(product_quantity) AS product_quantity_count,
    'Web' AS location
FROM
    orders_table
WHERE
    store_code LIKE 'WEB%'

UNION ALL

-- Offline Sales
SELECT
    COUNT(*) AS number_of_sales,
    SUM(product_quantity) AS product_quantity_count,
    'Offline' AS location
FROM
    orders_table
WHERE
    store_code NOT LIKE 'WEB%';