# Multinational Retail Data Centralisation project

## Table of Contents
- [Project Description](#project-description)
- [Entity Relationship Diagram](#entity-relationship-diagram-of-completed-database)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [License](#license)

## Project Description
This project focuses on extracting, cleaning, and processing data from various sources, including AWS RDS, S3 buckets, and external APIs. The primary aim is to prepare the data for further analysis or database storage, ensuring data integrity and consistency.

The project has expanded to include database design and management for a multinational retail corporation. This includes the creation of a star-schema database, aiding in data centralisation. It involves designing tables, establishing relationships, and ensuring data integrity through primary and foreign key constraints.

Key additions include SQL scripts for table creation, data integrity enforcement, schema management, and complex queries for business insights. These developments enhance the project's aim to facilitate robust data analysis and storage, ensuring consistent and reliable data quality.

## Entity Relationship Diagram of Completed Database
![Entity Relationship diagram](<assets/entity-relationship-diagram.png>)


## Installation

1. **Database Setup:**
- Ensure PostgreSQL is installed and set up on your system.
- Use PGAdmin or a similar tool to manage your PostgreSQL database.
- Create a new database for this project in your PostgreSQL server.

2. **Clone the Repository:**
```
git clone https://github.com/Zarhad-01/Multinational-Retail-Data-Centralisation
cd Multinational-Retail-Data-Centralisation
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

## Database Tables

After the cleaning and processing steps, the database tables have been organized into two main folders to highlight the changes and improvements made:

- `completed-database-tables/`: This directory contains the final versions of the database tables after cleaning and optimization. If you're interested in the cleaned data ready for analysis or database storage, please refer to this folder.

- `original-database-tables/`: This directory holds the original versions of the database tables before cleaning. If you wish to see the data in its initial state or compare it with the cleaned versions, this is where you can find those files.

Feel free to explore these folders to better understand the transformations applied to the data as part of the Multinational Retail Data Centralisation project.

## Usage
### Python Scripts:
To run the data cleaning and extraction scripts, execute the `main.py` file:
```
python python/main.py
```
This will trigger the data extraction, cleaning, and uploading processes as defined in the main function.

### SQL Scripts:
Use PGAdmin or a similar PostgreSQL client to run the SQL scripts in the following order:
1. Run `1_orders_table.sql` to set up the orders table.
2. Execute scripts `2_dim_users_table.sql` through `7_card_details.sql` to set up the respective dimension tables.
3. Apply `8_primary_keys.sql` to add primary keys to the dimension tables.
4. Finally, run `9_star_schema.sql` to establish the foreign key relationships and complete the star-schema.
5. Additional complex queries such as `1_stores_by_country.sql`, `2_most_stores_location.sql`, `3_sales_by_month.sql`, `4_online_sales.sql`, `5_percentage_sales.sql`, `6_sales.sql`, `7_staff_headcount.sql`, `8_german_stores.sql`, and `9_sales_speed.sql` provide deep insights into various business metrics.


## File Structure
The project is organized into the following directories and files:

### Python Scripts:
- `python/` - Contains Python scripts for data cleaning and extraction.
  - `data_cleaning.py` - Defines the `DataCleaning` class with methods to clean data.
  - `data_extraction.py` - Contains the `DataExtractor` class for extracting data from various sources.
  - `database_utils.py` - Provides the `DatabaseConnector` class for database operations.
  - `db_creds_local.yaml` - Stores local database credentials (do not commit to version control).
  - `db_creds.yaml` - Stores remote database credentials (ensure this is in `.gitignore`).
  - `main.py` - Main script to run the data processing tasks.

### SQL Scripts:
- `sql-queries/`
  - `create_database_schema/` - Scripts for creating the database schema.
    - `1_orders_table.sql` - Creates the orders table.
    - `2_dim_users_table.sql` - Sets up the users table.
    - `3_store_details.sql` - Defines the store details table.
    - `4_products.sql` - Creates the products table.
    - `5_products.sql` - Additional script for product-related operations.
    - `6_date_times.sql` - Sets up the event date table.
    - `7_card_details.sql` - Defines the card details table.
    - `8_primary_keys.sql` - Adds primary keys to the tables.
    - `9_star_schema.sql` - Finalizes the star schema with foreign key constraints.
  - `querying_the_data/` - Scripts for querying the database to extract insights.
    - `1_stores_by_country.sql` - Retrieves store count by country.
    - `2_most_stores_location.sql` - Finds the location with the most stores.
    - `3_sales_by_month.sql` - Determines sales figures by month.
    - `4_online_sales.sql` - Calculates online sales.
    - `5_percentage_sales.sql` - Computes the percentage of total sales.
    - `6_sales.sql` - General sales query.
    - `7_staff_headcount.sql` - Counts staff by location.
    - `8_german_stores.sql` - Assesses German store sales.
    - `9_sales_speed.sql` - Evaluates the speed of sales.

### Database Tables:
- `completed-database-tables/` - Contains the cleaned and optimized versions of the database tables.
  - `dim_card_details.csv` - Cleaned card details data.
  - `dim_date_times.csv` - Cleaned date and time data.
  - `dim_products.csv` - Cleaned products data.
  - `dim_store_details.csv` - Cleaned store details data.
  - `dim_user_table.csv` - Cleaned user data.
  - `orders_table.csv` - Cleaned orders data.
- `original-database-tables/` - Contains the original, uncleaned versions of the database tables.
  - `card_details.csv` - Original card details data.
  - `dates.csv` - Original date and time data.
  - `orders.csv` - Original orders data.
  - `products.csv` - Original products data.
  - `stores.csv` - Original store details data.
  - `user_data.csv` - Original user data.

### Assets:
- `assets/`
  - `entity-relationship-diagram.png` - Visual representation of the database schema.

### Miscellaneous:
- `.gitignore` - Specifies files to be ignored by version control.
- `README.md` - Project documentation in Markdown format.
- `Blank diagram.png` - A blank diagram for potential use in documentation or presentation materials.


## License
[MIT License](LICENSE)
