from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy
import os

class SpotipyClient:
    
    __default_scope = 'user-read-recently-played'
    
    @staticmethod
    def general_data_client() -> spotipy.Spotify:
        return spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=os.environ.get('CLIENT_ID'),
                client_secret=os.environ.get('CLIENT_SECRET')
            )
        )

    def authorization_flow_client(self, scope: str = None) -> spotipy.Spotify:
        return spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.getenv('CLIENT_ID'),
                client_secret=os.getenv('CLIENT_SECRET'),
                redirect_uri=os.getenv('REDIRECT_URI'),
                scope=self.__default_scope if not scope else scope,
                open_browser=False
            )
        )