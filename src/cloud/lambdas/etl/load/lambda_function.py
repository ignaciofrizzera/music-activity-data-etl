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
    
    def __merge_data_from_same_date(existing_data: pd.DataFrame, new_data: pd.DataFrame) -> pd.DataFrame:
        existing_data.set_index('song_id', inplace=True, drop=False)
        new_data.set_index('song_id', inplace=True, drop=False)

        new_songs = []
        for song_id, curr_song_data in new_data.iterrows():
            if song_id in existing_data.index:
                updated_played_at = list(set(existing_data.at[song_id, 'played_at']).union(set(curr_song_data['played_at'])))
                existing_data.at[song_id, 'played_at'] = updated_played_at
            else:
                new_songs.append(curr_song_data)
        
        existing_data.reset_index(inplace=True)
        
        if new_songs:
            existing_data = pd.concat([existing_data, pd.DataFrame(new_songs)])

        return existing_data

    # Split songs by dates.
    songs_by_date = {}
    for song in data:
        song_dates = {}
        # split each played_at to it's corresponding date, in case there are mixed days in the song data 
        # (eg: 16th and 17th, 23:00 crawler data and 00:00 crawler data)
        for played_at in song['played_at']:
            played_at_date = __get_date_from_played_at(played_at)
            song_dates.setdefault(played_at_date, []).append(played_at)
        # add the song with it's played_ats to the corresponding date
        for song_date, played_at_for_date in song_dates.items():
            song_for_date = song.copy()
            song_for_date['played_at'] = played_at_for_date
            songs_by_date.setdefault(song_date, []).append(song_for_date)
    
    for date_key, songs_from_date in songs_by_date.items():
        existing_data = clean_file_repository.get(date_key)
        new_data = pd.DataFrame(songs_from_date)
        
        if not existing_data.empty:
            new_data = __merge_data_from_same_date(existing_data, new_data)
        
        clean_file_repository.post(date_key, new_data.to_json(orient='records'))
    
    # Once we generate our daily cleaned data, we proceed to delete all the intermediate files:
    # hourly reports, unstructured_report, structured_report.
    raw_file_repository.delete()

def lambda_handler(event, context):
    load()
