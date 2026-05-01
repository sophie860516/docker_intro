# Taxi data ingestion

## Run PostgreSQL in a container

```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

This creates a named volume (`ny_taxi_postgres_data`) for future use.

To inspect the actual host path for the volume:

```bash
docker volume inspect ny_taxi_postgres_data
```

## Use `pgcli` to interact with the database

```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

## Run the automated data ingestion

Run the Python ingestion script with the appropriate parameters:

```bash
uv run python NYC_TAXI_DATA_V1.py \
  --year=2021 \
  --month=1 \
  --chunksize=10000 \
  --pg-user=root \
  --pg-password=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_data_v1
```

## Use pgAdmin

Use pgAdmin to access the `ny_taxi` database in a browser.

If you need to run pgAdmin in Docker, start it on a network that can reach the PostgreSQL container and map a host port, for example:

```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase
  postgres:18
```

```bash
docker run -d \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

If you want to run the integration script, make sure to use the same virtual network
```bash
uv run python NYC_TAXI_DATA_V1.py \
  --network=pg-network \
  --year=2021 \
  --month=1 \
  --chunksize=10000 \
  --pg-user=root \
  --pg-password=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_data_v1
```

## docker-compose
The docker-compose.yaml file allows launching multiple containers silmultaneously.

`#`To run in foreground
```bash
docker-compose up
```

`#`To run in background
```bash
docker-compose up -d
```
`#`To stop the containers
*Workspace cleaned up, containers paused and internal network removed. Data stay on hard drive* 
```bash
docker-compose down
```
`#`To remove volumes
*Removing volumes wipes the database*
```bash
docker-compose down -v
```