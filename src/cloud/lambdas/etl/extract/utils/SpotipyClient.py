from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy
import os

class SpotipyClient:
    
    @staticmethod
    def general_data_client() -> spotipy.Spotify:
        return spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=os.environ.get('CLIENT_ID'),
                client_secret=os.environ.get('CLIENT_SECRET')
            )
        )