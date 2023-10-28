from src.extract.extract import extract
from src.transform.transform import transform
from src.load.load import load

if __name__ == '__main__':
    """ For the time being, testing like this. Once the ETL functions are done, will decide to make the 
    airflow DAG or look into AWS resources to do everything there.
    """
    
    extract()
    # transform() -> TODO
    # load() -> TODO