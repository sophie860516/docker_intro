#!/usr/bin/env python
# coding: utf-8
#The script reads data in chunks to avoid memory issues while reading large csv files. 
# The data is then inserted into a PostgreSQL database.


from calendar import month

import click
import pandas as pd
from tqdm.auto import tqdm
from sqlalchemy import create_engine

#define data types for each column in the csv file
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]





@click.command()
@click.option('--year', default=2021, type=int, help='Year for the data')
@click.option('--month', default=1, type=int, help='Month for the data')
@click.option('--chunksize', default=10000, type=int, help='Chunk size for reading CSV')
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-password', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database')
def run(year, month, chunksize, pg_user, pg_password, pg_host, pg_port, pg_db):
    #ingest data in csv file into postgres
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{prefix}yellow_tripdata_{year}-{month:02d}.csv.gz'

    #create engine for connection
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')

    #create iterator
    df_iter = pd.read_csv(
        prefix + 'yellow_tripdata_2021-01.csv.gz', 
        dtype= dtype,
        parse_dates = parse_dates,
        iterator=True,
        chunksize= chunksize
    )
    first = True
    for df_chunk in tqdm(df_iter):
        if(first):
            df_chunk.head(0).to_sql(name = 'yellow_taxi_data',con=engine, if_exists='replace')
            first = False
        else:
            df_chunk.to_sql(name = 'yellow_taxi_data',con=engine, if_exists='append')

if __name__ == "__main__":
    run()
    print("Data insertion completed")




"""
Example usage of passing parameters to the script through command line:
uv run NYC_TAXI_DATA_V1.py \
    --year=2021 \
    --month=1 \
    --chunksize=10000 \
    --pg-user=root \
    --pg-password=root \
    --pg-host=localhost \
    --pg-port=5432 \
    --pg-db=ny_taxi
"""