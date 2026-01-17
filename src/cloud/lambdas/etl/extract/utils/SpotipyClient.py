import os

from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy


class SpotipyClient:

    @staticmethod
    def general_data_client() -> spotipy.Spotify:
        """
        Initialize a general purpose client of Spotipy.

        Returns:
            spotipy.Spotify: Spotipy client instance.
        """
        return spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=os.environ.get('CLIENT_ID'),
                client_secret=os.environ.get('CLIENT_SECRET')
            )
        )
