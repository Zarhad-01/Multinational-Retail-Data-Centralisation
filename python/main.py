from data_cleaning import DataCleaning
from data_extraction import DataExtractor
from database_utils import DatabaseConnector
from sqlalchemy import create_engine

# Global Variables
CONNECTOR = DatabaseConnector()
EXTRACTOR = DataExtractor()
CLEANER = DataCleaning()
CREDS = CONNECTOR.read_local_creds()
if CREDS:
    ENGINE = create_engine(f"postgresql+psycopg2://{CREDS['USER']}:{CREDS['PASSWORD']}@{CREDS['HOST']}:{CREDS['PORT']}/{CREDS['DATABASE']}")

def main():
    dim_users()
    dim_card_details()
    dim_store_details()
    dim_products()
    orders_table()
    dim_date_times()

def dim_users():
    remote_engine = CONNECTOR.init_db_engine()
    tables = CONNECTOR.list_db_tables(remote_engine)

    user_data = EXTRACTOR.read_rds_table(tables[1], remote_engine)
    clean_user_data = CLEANER.clean_user_data(user_data)
    CONNECTOR.upload_to_db(clean_user_data, "dim_user_table", ENGINE)

def dim_card_details():
    card_data = EXTRACTOR.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
    clean_card_data = CLEANER.clean_card_data(card_data)
    CONNECTOR.upload_to_db(clean_card_data, "dim_card_details", ENGINE) 

def dim_store_details():
    api_key = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
    num_of_store_endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores"
    store_details_endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/"

    number_stores = EXTRACTOR.list_number_of_stores(num_of_store_endpoint, api_key)
    stores = EXTRACTOR.retrieve_stores_data(store_details_endpoint, number_stores, api_key)
    clean_stores = CLEANER.clean_store_data(stores)
    CONNECTOR.upload_to_db(clean_stores, 'dim_store_details', ENGINE)

def dim_products():
    s3_data = EXTRACTOR.extract_from_s3()
    s3_data = CLEANER.convert_product_weights(s3_data)
    clean_s3_data = CLEANER.clean_products_data(s3_data)
    CONNECTOR.upload_to_db(clean_s3_data, 'dim_products', ENGINE)

def orders_table():
    remote_engine = CONNECTOR.init_db_engine()
    tables = CONNECTOR.list_db_tables(remote_engine)
    orders_df = EXTRACTOR.read_rds_table(tables[2], remote_engine)

    clean_orders = CLEANER.clean_orders_data(orders_df)
    CONNECTOR.upload_to_db(clean_orders, 'orders_table', ENGINE)

def dim_date_times():
    address = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'

    date_data = EXTRACTOR.extract_from_s3_JSON(address)
    cleaned_date_data = CLEANER.clean_date_table(date_data)
    CONNECTOR.upload_to_db(cleaned_date_data, 'dim_date_times', ENGINE)


if __name__ == "__main__":
    main()