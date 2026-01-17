from typing import Any, Dict

from spotipy.exceptions import SpotifyException
import spotipy


class SummarizedTrack:

    def __str__(self) -> str:
        if self.data:
            return f"{self.data}"
        return ""

    def __init__(self, spotify_client: spotipy.Spotify, song_data: Dict[str, str]):
        """
        Initialize a SummarizedTrack instance based on a song metadata.

        Args:
            spotify_client (spotipy.Spotify): Spotipy client instance.
            song_data (Dict[str, str]): Song metadata.

        Attributes:
            data (Dict[str, Any]): Data about the summarized track.
            track_id (str): ID of the summarized track.
            __spotify_client (spotipy.Spotify): Spotipy client.

        Raises:
            ValueError: If initialization fails due to invalid data provided or spotipy client failure.
        """
        self.data = {}
        self.__spotify_client = spotify_client

        try:
            track_id = song_data['track_id']
            track_data = self.__spotify_client.track(track_id)
            track_data = self.__get_track_data(track_data)
            song_data.update(track_data)

            self.track_id = track_id
            self.data = song_data
        except (KeyError, SpotifyException) as e:
            raise ValueError(f"Failed to summarize track: {e}")

    @staticmethod
    def __get_track_data(
        track_response_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate and retrieve the track data based on the response data provided.

        Args:
            track_response_data (Dict[str, Any]): Response containing the track data.

        Returns:
            (Dict[str, Any]): Dictionary containing the cleaned data of the track.

        Raises:
            KeyError: If any of the expected keys is not present in the response data.
        """
        clean_data = {
            'explicit': track_response_data['explicit'], 
            'popularity': track_response_data['popularity']
        }
        clean_data['album'] = track_response_data['album']['name']
        track_album_image = track_response_data['album']['images'][0]
        clean_data['album_cover'] = track_album_image['url']
        clean_data['album_cover_height'] = track_album_image['height']
        clean_data['album_cover_width'] = track_album_image['width']
        return clean_data

    def get_data(self) -> Dict[str, Any]:
        """
        Retrieve the data of the SummarizedTrack.

        Returns:
            (Dict[str, Any]): Dictionary containing all the information about the track.
        """
        return self.data
