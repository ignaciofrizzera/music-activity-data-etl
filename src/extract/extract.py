"""
    Extract will have 4 steps:
        1) Retrieve the songs listened in the whole day.
        2) For each retrieved song, gather all the data related to it from the Spotify API.
        3) For each retrieved song, gather its lyrics from the Genius API.
        4) Dump the data in s3.
"""

from src.utils.SpotipyClient import SpotipyClient
from src.utils.SummarizedTrack import SummarizedTrack
from datetime import datetime, timedelta
from typing import Dict
import pytz
import time as tm

def extract():
    __timedelta = -3
    __timezone = 'America/Argentina/Buenos_Aires'
    
    def get_daily_songs():
        def transform_to_timezone(date: str) -> str:
            argentina_time = datetime.fromisoformat(date) + timedelta(hours=__timedelta)
            return argentina_time.strftime("%Y-%m-%d %H:%M")
        
        def calculate_unix_timestamp() -> int:
            return int(tm.time())
        
        def get_basic_info_from_song(song_data: Dict, played_at: str) -> Dict[str, str]:
            return {
                'track_id': song_data['id'],
                'track_name': song_data['name'],
                'track_artist': ', '.join([artist_data['name'] for artist_data in song_data['artists']]),
                'played_at': played_at
            }
        
        client = SpotipyClient().authorization_flow_client()
        max_limit = 50
        recently_played_response = client.current_user_recently_played(
            limit=max_limit, after=calculate_unix_timestamp())

        songs_data = []
        curr_date = datetime.now(pytz.timezone(__timezone)).date()

        songs_by_day = [[curr_date, songs_data]]
        
        for item in recently_played_response['items']:
            normalized_played_at = transform_to_timezone(item['played_at'])
            song_date = datetime.fromisoformat(normalized_played_at).date()

            if curr_date != datetime.fromisoformat(normalized_played_at).date():
                print(f"Changing date from {curr_date} to {song_date}")
                curr_date = song_date
                songs_data = []
                songs_by_day.append([curr_date, songs_data])
            
            summarized_audio_track = SummarizedTrack(
                get_basic_info_from_song(item['track'], normalized_played_at))
            songs_data.append(summarized_audio_track)

        return songs_by_day
    
    """
        Spotify will only give us the last 50 recently played, no matter what,
        so using cursors, before/after, won't work, and we'll just stick to 50 songs.
    """
    songs = get_daily_songs()
    
    for whole_day_data in songs:
        print(f"Songs for date: {whole_day_data[0]}")
        for song in whole_day_data[1]:
            print(song.get_general_data())