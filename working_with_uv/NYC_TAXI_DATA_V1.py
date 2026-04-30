#!/usr/bin/env python
# coding: utf-8


from calendar import month

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



#assgine parameters 
year=2021
month=1
chunksize= 10000

def run():
    #ingest data in csv file into postgres
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{prefix}yellow_tripdata_{year}-{month:02d}.csv.gz'

    #create engine for connection
    engine = create_engine('postgresql+psycopg://root:root@localhost:5432/ny_taxi')

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





