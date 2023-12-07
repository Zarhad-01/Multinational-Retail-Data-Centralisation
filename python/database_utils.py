import yaml
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import inspect

class DatabaseConnector:

    @staticmethod
    def read_db_creds():
        try:
            with open('python/db_creds.yaml', 'r') as stream:
                return yaml.safe_load(stream)
        except FileNotFoundError:
            print("python/db_creds.yaml file not found.")
            return None
        except yaml.YAMLError as err:
            print(f"Error in YAML: {err}")
            return None

    def read_local_creds(self):
        try:
            with open('python/db_creds_local.yaml', 'r') as stream:
                return yaml.safe_load(stream)
        except FileNotFoundError:
            print("python/db_creds.yaml file not found.")
            return None
        except yaml.YAMLError as err:
            print(f"Error in YAML: {err}")
            return None
    
    def init_db_engine(self):
        creds = self.read_db_creds()

        if creds:
            engine = create_engine(f"postgresql+psycopg2://{creds['RDS_USER']}:{creds['RDS_PASSWORD']}@{creds['RDS_HOST']}:{creds['RDS_PORT']}/{creds['RDS_DATABASE']}")
            return engine
        else:
            return None
    
    def list_db_tables(self, engine):
        inspector = inspect(engine)
        return inspector.get_table_names()

    def upload_to_db(self,df,name,engine):
        df.to_sql(name, engine, if_exists='replace')
    

# if __name__ == '__main__':
    # dc = DatabaseConnector()
    # creds = dc.read_db_creds()
# 
    # print(creds)
    # print(type(creds))
    # print(type(dc.init_db_engine()))
    # print(type(dc.list_db_tables()))
# 
    # tables_list = dc.list_db_tables()
# 
    # with dc.init_db_engine().begin() as conn:
        # table = pd.read_sql_table(tables_list[1], con=conn)
    # print(table)