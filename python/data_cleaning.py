import pandas as pd
import numpy as np
import os
import re
from database_utils import DatabaseConnector
from data_extraction import DataExtractor

class DataCleaning:

    def clean_user_data(self, legacy_users_data=None):
        """
        This function is used to clean the users data table.
        If legacy_users_data is not provided, it extracts data from the 'legacy_users' table.
        """
        if legacy_users_data is None:
            legacy_users_data = DataExtractor().read_rds_table('legacy_users')

        # Replace 'NULL' with NaN and drop rows with NaN in specific columns
        legacy_users_data.replace('NULL', np.nan, inplace=True)
        legacy_users_data.dropna(subset=['date_of_birth', 'join_date'], inplace=True)

        # Handle date conversion with error coercion
        legacy_users_data['date_of_birth'] = pd.to_datetime(legacy_users_data['date_of_birth'], infer_datetime_format=True, errors='coerce')
        legacy_users_data['join_date'] = pd.to_datetime(legacy_users_data['join_date'], infer_datetime_format=True, errors='coerce')

        # Remove duplicates based on email address
        legacy_users_data = legacy_users_data.drop_duplicates(subset=['email_address'])

        # Fix phone numbers using regex
        regex_expression = r'^(?:(?:\(?(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?(?:\(?0\)?[\s-]?)?)|(?:\(?0))(?:(?:\d{5}\)?[\s-]?\d{4,5})|(?:\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3}))|(?:\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4})|(?:\d{2}\)?[\s-]?\d{4}[\s-]?\d{4}))(?:[\s-]?(?:x|ext\.?|\#)\d{3,4})?$'
        legacy_users_data.loc[~legacy_users_data['phone_number'].str.match(regex_expression), 'phone_number'] = np.nan


        # Drop rows filled with wrong information
        legacy_users_data.drop(legacy_users_data.columns[0], axis=1, inplace=True)

        return legacy_users_data

    def clean_card_data(self, card_data_table=None):
        """
        This function is used to clean the card data table.
        If card_data_table is not provided, it extracts data from the provided PDF link.
        """
        if card_data_table is None:
            card_data_table = DataExtractor().retrieve_pdf_data("https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf")

        # Replace 'NULL' with NaN and remove non-numeric characters from 'card_number'
        card_data_table.replace('NULL', np.nan, inplace=True)
        card_data_table['card_number'] = card_data_table['card_number'].astype(str).str.replace('\W', '', regex=True)

        # Remove rows where 'card_number' contains alphabetic characters, question marks, or is not 16 characters long
        card_data_table = card_data_table[~card_data_table['card_number'].str.contains('[a-zA-Z?]', na=False) & (card_data_table['card_number'].str.len() == 16)]


        # Convert 'date_payment_confirmed' to datetime and handle errors
        card_data_table['date_payment_confirmed'] = pd.to_datetime(card_data_table['date_payment_confirmed'], infer_datetime_format=True, errors='coerce')

        # Drop rows with NaN in 'card_number' and 'date_payment_confirmed'
        card_data_table.dropna(subset=['card_number', 'date_payment_confirmed'], how='any', inplace=True)

        return card_data_table

    def clean_store_data(self, store_data_table):
        """
        Clean the store data table
        """

        store_data_table = store_data_table.reset_index(drop=True)

        store_data_table.replace('NULL',np.nan,inplace=True)

        store_data_table.drop(store_data_table.columns[0], axis=1,inplace=True)
        store_data_table.drop(columns='lat',inplace=True)
        
        store_data_table['opening_date'] = pd.to_datetime(store_data_table['opening_date'], errors='coerce')
        store_data_table['staff_numbers'] = pd.to_numeric(store_data_table['staff_numbers'], errors='coerce')
        store_data_table.dropna(subset=['staff_numbers'],axis=0,inplace=True)

        store_data_table['continent'] = store_data_table['continent'].str.replace('eeEurope', 'Europe')
        store_data_table['continent'] = store_data_table['continent'].str.replace('eeAmerica', 'America')

        return store_data_table
    
    def convert_product_weights(self, products_df):
        """
        Converts weights in the products DataFrame into kilograms.

        Args:
        products_df (DataFrame): DataFrame of products.

        Returns:
        DataFrame: Updated DataFrame with weights converted to kilograms.
        """
        conversion_factors = {'kg': 1, 'g': 0.001, 'ml': 0.001, 'oz': 0.0283495}

        def convert_weight(weight):
            numeric_part = ''.join([char for char in weight if char.isdigit() or char == '.'])
            if not numeric_part:
                return None
            numeric_weight = float(numeric_part)
            for unit in conversion_factors:
                if unit in weight:
                    return numeric_weight * conversion_factors[unit]
            return None

        products_df['weight'] = products_df['weight'].apply(convert_weight)
        return products_df

    def clean_products_data(self, df):
        """
        Cleans and processes product data.

        Args:
            df (pandas.DataFrame): The product data.

        Returns:
            pandas.DataFrame: The cleaned and processed product data.
        """

        # Drop first unnamed column if it exists
        if 'Unnamed: 0' in df.columns:
            df.drop('Unnamed: 0', axis=1, inplace=True)

        # Replace 'NULL' with NaN and drop rows with NaN values
        df.replace('NULL', np.nan, inplace=True)
        df.dropna(inplace=True)

        # Convert product prices to numeric values
        df['product_price'] = pd.to_numeric(df['product_price'].str.slice(1), errors='coerce').round(2)

        # Convert date_added to datetime and drop rows with NaN in 'date_added'
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
        df.dropna(subset=['date_added'], inplace=True)

        # UUID validation
        uuid_pattern = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
        df = df[df["uuid"].apply(lambda x: bool(re.match(uuid_pattern, str(x))))]

        # EAN numbers validation (ensure they are 13 digits long)
        df['EAN'] = df['EAN'].astype(str)
        df = df[df['EAN'].str.len() == 13]

        # Reset index
        df.reset_index(drop=True, inplace=True)

        return df

    def clean_orders_data(self, df):
        """
        Cleans and processes order data.

        Args:
            df (pandas.DataFrame): The order data.

        Returns:
            pandas.DataFrame: The cleaned and processed order data.
        """
        # Removing specified columns
        columns_to_remove = ['first_name', 'last_name', '1', 'level_0']
        df.drop(columns=columns_to_remove, inplace=True, errors='ignore')

        # Set index if 'index' column exists
        if 'index' in df.columns:
            df.set_index(['index'], inplace=True)

        return df

    def clean_date_table(self, date_table):
        """
        Cleans and processes date table data.

        Args:
            date_table (pandas.DataFrame): The date table data.

        Returns:
            pandas.DataFrame: The cleaned and processed date table data.
        """
        date_table['year'] = pd.to_datetime(date_table['year'], errors='coerce').dt.year.convert_dtypes()
        date_table['month'] = pd.to_datetime(date_table['month'], errors='coerce', format='%m').dt.month.convert_dtypes()
        date_table['day'] = pd.to_datetime(date_table['day'], errors='coerce', format='%d').dt.day.convert_dtypes()

        date_table['timestamp'] = pd.to_datetime(date_table['timestamp'], errors='coerce', format='%H:%M:%S').dt.time

        # Validating time periods
        valid_period = ["Late_Hours", "Morning", "Midday", "Evening"]
        date_table = date_table[date_table['time_period'].isin(valid_period)]

        date_table.dropna(inplace=True)

        return date_table

    def save_cleaned_data_to_file(self, df, table_name):
        # Create a directory 'python' if it doesn't exist
        os.makedirs('python', exist_ok=True)
        file_path = f'python/cleaned_data_{table_name}.txt'
        with open(file_path, 'w') as file:
            df.to_string(file)
        print(f"Cleaned data saved to {file_path}")

if __name__ == '__main__':
    tables_to_clean = ["legacy_store_details", "legacy_users", "orders_table"]
    db_connector = DatabaseConnector()
    extractor = DataExtractor(db_connector)
    legacy_users_table = extractor.read_rds_table('legacy_users')

    legacy_users_table.info()

    dc = DataCleaning()
    # cleaned_data = dc.clean_user_data(legacy_users_table)
    # dc.save_cleaned_data_to_file(cleaned_data, "legacy_users")
    # print(cleaned_data.info())

    clean_card_data = dc.clean_card_data()
    print(type(clean_card_data))
    print(clean_card_data.to_string())
    db_connector.upload_to_db()