-- Query to determine sales by store type in Germany
SELECT
    ROUND(SUM(dpr.product_price * otable.product_quantity)::numeric, 2) AS total_sales, -- Calculating total sales
    dsd.store_type, 
    dsd.country_code 
FROM
    orders_table otable
JOIN
    dim_store_details dsd ON otable.store_code = dsd.store_code
JOIN
    dim_products dpr ON otable.product_code = dpr.product_code
WHERE
    dsd.country_code = 'DE'
GROUP BY
    dsd.store_type, dsd.country_code
ORDER BY
    total_sales DESC;
