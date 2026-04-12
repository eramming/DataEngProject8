# DataEngProject8
Class project for JHU 685.652 Data Engineering for Spring '26.


## How To Run
Dev mode allows for frequent changes to the code base that are immediately reflected in the active server.

Production mode is for the polished final product. It is harder to debug and takes longer for changes to be incorporated (since docker image must be rebuilt each time).
### Local Dev Mode
Quick summary of what we will do:

1. Install `pipenv` as alternative to `pip` for managing Python packages
2. Install necessary packages into our Python virtual environment
3. Enter our virtual environment
4. Launch any supporting services, like a database.
5. Launch our server (to be able to see what exists in our db) 

Install `pipenv` virtual environment manager. It's just a different flavor of `pip`.

`pip install pipenv`

Install already specified packages using `pipenv`.

`pipenv sync`

Enter your python virtual environment.

`pipenv shell`

Launch supporting services.

`docker compose -f docker-compose-dev.yml up -d`

Launch the server. It auto-restarts when you make changes.

`cd ../backend`
`uvicorn SportsApp:app --reload`

To exit/shutdown.

`control c` to shutdown server

`docker compose -f docker-compose-dev.yml down` to shutdown supporting services

`exit` to exit virtual environment

### Production Mode
To launch:

`docker compose up -d`

DAG will run ingest pipeline, but run this for manual ingestion:

`docker compose exec airflow-webserver airflow dags trigger mls_ingest_pipeline` 

To view available endpoints, run: 

`http://localhost:8000/docs` 

To see a combined view of our underlying Postgres tables, run: 

`http://localhost:8000/view` 

To exit:

`docker compose down`