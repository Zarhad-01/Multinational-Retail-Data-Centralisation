import pandas as pd
import tabula as tb
import requests
import json
import boto3

from database_utils import DatabaseConnector
class DataExtractor:

    def __init__(self, db_connector = DatabaseConnector()):
        self.db_connector = db_connector

    def read_rds_table(self, table, engine):
        with engine.connect() as connection:
            return pd.read_sql_table(table, connection)
    
    def print_table_attributes(self, table_name):
        engine = self.db_connector.init_db_engine()
        if engine:
            df = pd.read_sql_table(table_name, engine)
            print(f"Attributes of {table_name}:")
            print(df.columns.tolist())
        else:
            print("Database engine not initialized.")
    
    def retrieve_pdf_data(self,link):
        dfs = tb.read_pdf(link, stream=True)
        print(type(dfs))
        print(len(dfs))
        return dfs[0]

    def list_number_of_stores(self, endpoint, key):
        """
        List the number of stores
        """
        response = requests.get(endpoint,headers=key)
        info = response.text
        info_json = json.loads(info)
        number_of_stores = info_json['number_stores']
        return number_of_stores
    
    def retrieve_stores_data(self,endpoint, number_of_stores, key):
        """
        Retrieve the data in the stores
        """
        stores_data = []

        for i in range(number_of_stores):
            response = requests.get(f"{endpoint}{i}", headers=key)
            info = response.text
            info_json = json.loads(info)
            stores_data.append(info_json)

        stores_df = pd.DataFrame(stores_data)
        return stores_df

    def extract_from_s3(self):
        s3_client = boto3.client("s3")
        
        response = s3_client.get_object(Bucket='data-handling-public', Key='products.csv')

        res   = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if res == 200:
            return pd.read_csv(response.get("Body"))
        else:
            print(f"Error {res}")
    
    def extract_from_s3_JSON(self, url):
        """
        Retrieves data from a CSV or JSON file in an S3 bucket via an HTTPS URL and returns it as a DataFrame.

        Args:
            url (str): HTTPS URL to the S3 object (e.g., 'https://bucket-name.s3.Region.amazonaws.com/key-name').

        Returns:
            pandas.DataFrame: Data from the S3 file.

        Raises:
            ValueError: If file type is not JSON.
            Exception: For S3 access or file reading errors.
        """
        # Extract bucket name and path from URL
        assert url.startswith('https://'), "URL must start with 'https://'"
        split_url = url.split('/')
        bucket = split_url[2].split('.')[0]
        path = '/'.join(split_url[3:])
        file_type = path.split('.')[-1]

        s3 = boto3.client('s3')

        try:
            obj = s3.get_object(Bucket=bucket, Key=path)
            if file_type.lower() == 'json':
                df = pd.read_json(obj['Body'])
            else:
                raise ValueError('Unsupported file type. Only CSV and JSON files are supported.')

            return df

        except Exception as e:
            raise Exception(f"Error extracting data from S3: {e}")

# if __name__ == '__main__':
    # db_connector = DatabaseConnector()
    # extractor = DataExtractor(db_connector)
# 
    # print(extractor.read_rds_table("orders_table"))
# 
    # for table in ['legacy_store_details', 'legacy_users', 'orders_table']:
        # extractor.print_table_attributes(table)
    # 
    # df = extractor.retrieve_pdf_data("https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf")
    # print(type(df))