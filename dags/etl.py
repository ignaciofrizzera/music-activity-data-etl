from src.etl.extract.extract import extract
from src.etl.transform.transform import transform
from src.etl.load.load import load
from airflow.decorators import dag, task
import pendulum

@dag(
    dag_id="daily_data_spotify",
    schedule="30 23 * * *", # runs every day at 23:30 PM
    start_date=pendulum.datetime(2023, 11, 13, tz="UTC-3"), # next week
)
def run_etl():

    @task()
    def run_extract():
        extract()
    
    @task()
    def run_transform():
        transform()
    
    @task()
    def run_load():
        load()
    
    run_extract()
    run_transform()
    run_load()

    run_extract > run_transform > run_load