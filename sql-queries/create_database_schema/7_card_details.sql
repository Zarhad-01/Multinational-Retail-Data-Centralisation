-- Updating the dim_card_details table

-- +------------------------+-------------------+--------------------+
-- |    dim_card_details    | current data type | required data type |
-- +------------------------+-------------------+--------------------+
-- | card_number            | TEXT              | VARCHAR(19)        |
-- | expiry_date            | TEXT              | VARCHAR(5)         |
-- | date_payment_confirmed | TEXT              | DATE               |
-- +------------------------+-------------------+--------------------+

ALTER TABLE dim_card_details
    ALTER COLUMN card_number            TYPE VARCHAR(19),
    ALTER COLUMN expiry_date            TYPE VARCHAR(5),
    ALTER COLUMN date_payment_confirmed TYPE DATE;