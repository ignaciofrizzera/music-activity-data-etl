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
    
    # Split songs by dates.
    songs_by_date = {}
    for song in data:
        song_date = __get_date_from_played_at(song['played_at'])
        if not songs_by_date.get(song_date):
            songs_by_date[song_date] = []
        songs_by_date[song_date].append(song)
    
    for date_key, songs_from_date in songs_by_date.items():
        existing_df = clean_file_repository.get(date_key)
        new_data = pd.DataFrame(songs_from_date)
        if not existing_df.empty:
            new_data = pd.concat([existing_df, new_data])
        new_data.drop_duplicates(['track_id', 'played_at'], inplace=True)
        clean_file_repository.post(date_key, new_data.to_json(orient='records'))
    
    # Once we generate our daily cleaned data, we proceed to delete all the intermediate files.
    raw_file_repository.delete()

def lambda_handler(event, context):
    load()
