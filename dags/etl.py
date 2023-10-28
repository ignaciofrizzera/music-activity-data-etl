from airflow.decorators import dag, task
from src.extract.extract import extract
from src.transform.transform import transform
from src.load.load import load
import pendulum

# airflow is a pain to run on windows :(
@dag(
    schedule="0 0 * * *", # probably will be every 1 hour
    start_date=pendulum.datetime(2023, 10, 24, tz="UTC-3"),
)
def run_etl():
    """
    """

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