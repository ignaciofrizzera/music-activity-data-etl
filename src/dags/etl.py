from airflow.decorators import dag, task
from src.extract.extract import extract
from src.transform.transform import transform
from src.load.load import load


@dag()
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

run_etl()