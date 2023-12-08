# Multinational Retail Data Centralisation project

## Table of Contents
- [Project Description](#project-description)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [License](#license)

## Project Description
This project focuses on extracting, cleaning, and processing data from various sources, including AWS RDS, S3 buckets, and external APIs. The primary aim is to prepare the data for further analysis or database storage, ensuring data integrity and consistency.

Key learnings and challenges in this project include working with different data formats (CSV, JSON), handling database connections, and implementing data cleaning techniques using Pandas in Python.

This project now encompasses a comprehensive approach to data management, extending its reach to database design and management for a multinational retail corporation. The focus has expanded to include the creation of a star-schema database, aiding in data centralisation. This includes designing tables, establishing relationships, and ensuring data integrity through primary and foreign key constraints.

Key additions include SQL scripts for table creation, data integrity enforcement, and schema management. These developments enhance the project's aim to facilitate robust data analysis and storage, ensuring consistent and reliable data quality.

## Installation

1. **Database Setup:**
- Ensure PostgreSQL is installed and set up on your system.
- Use PGAdmin or a similar tool to manage your PostgreSQL database.
- Create a new database for this project in your PostgreSQL server.

2. **Clone the Repository:**
```
git clone [repository-url]
cd [repository-name]
```

3. **Install Required Python Packages:**
Ensure you have Python installed on your system. Then, install the required packages:
```
pip install pandas numpy sqlalchemy psycopg2 boto3 pyyaml tabula-py requests
```

3. **Database Configuration:**
- Create a PostgreSQL database.
- Update a `db_creds.yaml` file with your remote database credentials within the python folder.
- Update the `db_creds_local.yaml` file with your local database credentials within the python folder.

4. **AWS Configuration:**
- Ensure you have AWS credentials set up for accessing RDS and S3 services. This typically involves setting up `~/.aws/credentials`.

## Usage
### Python Scripts:
To run the data cleaning and extraction scripts, execute the `main.py` file:
```
python main.py
```
This will trigger the data extraction, cleaning, and uploading processes as defined in the main function.

### SQL Scripts:
Use PGAdmin or a similar PostgreSQL client to run the SQL scripts in the following order:
1. Run `1_orders_table.sql` to set up the orders table.
2. Execute scripts `2_dim_users_table.sql` through `7_card_details.sql` to set up the respective dimension tables.
3. Apply `8_primary_keys.sql` to add primary keys to the dimension tables.
4. Finally, run `9_star_schema.sql` to establish the foreign key relationships and complete the star-schema.

## File Structure
- `data_cleaning.py`: Contains the `DataCleaning` class with methods for cleaning various data tables.
- `data_extraction.py`: Includes the `DataExtractor` class for extracting data from RDS, S3, and APIs.
- `database_utils.py`: Defines the `DatabaseConnector` class for database connection and operations.
- `main.py`: The main script to run the data processing tasks.

## License
[MIT License](LICENSE)
