#Running postgres in a container
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \ --creates a named volume for future use 
  -p 5432:5432 \
  postgres:18

#connect to database using pgcli
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi 

#automated data integration
run the script NYC_TAXI_DATA_V1.py