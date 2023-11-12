from datetime import timedelta, datetime
from spotipy.oauth2 import SpotifyOAuth
from typing import Dict, List
import time as tm
import spotipy
import json
import os

def recently_played(event, context):
    __timedelta = -3
    __scope = 'user-read-recently-played'
    __max_limit = 50
    
    def authorization_flow_client() -> spotipy.Spotify:
        return spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.environ.get('CLIENT_ID'), # Set in the Lambda's env.
                client_secret=os.environ.get('CLIENT_SECRET'), # Set in the Lambda's env.
                redirect_uri=os.environ.get('REDIRECT_URI'), # Set in the Lambda's env.
                scope=__scope,
                open_browser=False
            )
        )
    
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
    client_auth_manager: SpotifyOAuth = client.auth_manager
    # Refresh token just in case.
    if client_auth_manager.is_token_expired(client_auth_manager.get_cached_token()):
        client_auth_manager.refresh_access_token(
            client_auth_manager.get_cached_token()['refresh_token'])
    
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