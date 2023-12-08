-- Query to calculate the total and percentage of sales by store type
WITH sales AS (
    SELECT
        dsd.store_type,
        SUM(dpr.product_price * otable.product_quantity) AS total_sales
    FROM
        orders_table otable
    JOIN
        dim_products dpr ON otable.product_code = dpr.product_code
    JOIN
        dim_store_details dsd ON otable.store_code = dsd.store_code
    GROUP BY
        dsd.store_type
)
SELECT 
    store_type,
    ROUND(SUM(total_sales)::numeric, 2) AS total_sales,
    ROUND((SUM(total_sales)::numeric * 100) / (SELECT SUM(total_sales) FROM sales)::numeric, 2) AS percentage_total
FROM
    sales
GROUP BY
    store_type
ORDER BY
    total_sales DESC;