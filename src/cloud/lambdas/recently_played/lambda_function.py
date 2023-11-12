from datetime import timedelta, datetime
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler
from typing import Dict, List
import time as tm
import spotipy
import json
import boto3
import os

def recently_played(event, context):
    __timedelta = -3
    __scope = 'user-read-recently-played'
    __max_limit = 50
    __cache_key = '.cache'
    __cache_path = f'/tmp/{__cache_key}'
    __cache_handler = CacheFileHandler(__cache_path)
    __bucket = 'spotipy-cache'
    
    def authorization_flow_client() -> spotipy.Spotify:
        return spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.environ.get('CLIENT_ID'),
                client_secret=os.environ.get('CLIENT_SECRET'),
                redirect_uri=os.environ.get('REDIRECT_URI'),
                scope=__scope,
                open_browser=False,
                cache_handler=__cache_handler
            )
        )
    
    def validate_token(auth: SpotifyOAuth):
        if not os.path.exists(__cache_path):
            s3 = boto3.client('s3')
            s3.download_file(Bucket=__bucket, Key=__cache_key, Filename=__cache_path)
        
        cached_token = __cache_handler.get_cached_token()
        if auth.is_token_expired(cached_token):
            auth.refresh_access_token(cached_token['refresh_token'])
            with open(__cache_path, 'r') as token_file:
                # update s3 cached content
                token = json.load(token_file)
                s3 = boto3.client('s3')
                s3.put_object(Bucket=__bucket, Key=__cache_key, Body=json.dumps(token))
    
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
    
    client = authorization_flow_client()
    validate_token(client.auth_manager)
    
    recently_played_response = client.current_user_recently_played(
        limit=__max_limit, after=calculate_unix_timestamp())

    songs: Dict[str, List[Dict[str, str]]] = {}
    for item in recently_played_response['items']:
        normalized_played_at = transform_to_timezone(item['played_at'])
        song_date = str(datetime.fromisoformat(normalized_played_at).date())
        
        if not songs.get(song_date):
            songs[song_date] = []
        
        songs.get(song_date).append(get_basic_info_from_song(
            item['track'], normalized_played_at))

    return {
        'run_at': transform_to_timezone(str(datetime.now())).replace('-', '/').replace(' ', '/'),
        'data': json.dumps(songs)
    }


def lambda_handler(event, context):
    return recently_played(event, context)