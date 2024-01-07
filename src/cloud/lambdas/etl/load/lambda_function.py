from s3.RawFileRepository import RawFileRepository
from s3.CleanFileRepository import CleanFileRepository
from s3.FileType import FileType
import pandas as pd


def load():
    raw_file_repository = RawFileRepository()
    data = raw_file_repository.get(FileType.STRUCTURED)
    clean_file_repository = CleanFileRepository()
    
    def __get_date_from_played_at(played_at: str) -> str:
        # "played_at": "2023-11-02 23:16"
        return played_at.split(' ')[0]
    
    def __is_subset(small_df: pd.DataFrame, big_df: pd.DataFrame, ) -> bool:
        # checks if the small_df is a subset of the big_df
        return len(small_df.merge(big_df, how='inner')) == len(small_df)
    
    def __drop_and_post(data: pd.DataFrame, date_key) -> None:
        data.drop_duplicates(['track_id', 'played_at'], inplace=True)
        clean_file_repository.post(date_key, data.to_json(orient='records'))

    # Split songs by dates.
    songs_by_date = {}
    for song in data:
        song_date = __get_date_from_played_at(song['played_at'])
        songs_by_date.setdefault(song_date, []).append(song)
    
    for date_key, songs_from_date in songs_by_date.items():
        existing_data = clean_file_repository.get(date_key)
        new_data = pd.DataFrame(songs_from_date)
        
        if existing_data.empty:
            # we still haven't loaded any data for this date, so we upload new data
            __drop_and_post(data=new_data, date_key=date_key)
        elif not __is_subset(small_df=new_data, big_df=existing_data):
            # the new data isn't a subset of the existing data, so we upload new data
            new_data = pd.concat([existing_data, new_data])
            __drop_and_post(data=new_data, date_key=date_key)
    
    # Once we generate our daily cleaned data, we proceed to delete all the intermediate files:
    # hourly reports, unstructured_report, structured_report.
    raw_file_repository.delete()

def lambda_handler(event, context):
    load()
