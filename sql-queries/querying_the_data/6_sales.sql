-- Query to find the top ten months with the highest sales historically
SELECT
    ROUND(SUM(dpr.product_price * otable.product_quantity)::numeric, 2) AS total_sales,
    ddt.year,
    ddt.month
FROM
    orders_table otable
JOIN
    dim_products dpr ON otable.product_code = dpr.product_code
JOIN
    dim_date_times ddt ON otable.date_uuid = ddt.date_uuid
GROUP BY
    ddt.year, ddt.month
ORDER BY
    total_sales DESC
LIMIT
    10;