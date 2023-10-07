from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from datetime import datetime
import spotipy
import time as tm
import os


def __setup_general_data_client() -> spotipy.Spotify:
    load_dotenv()
    return spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=os.getenv('CLIENT_ID'),
            client_secret=os.getenv('CLIENT_SECRET')
        )
    )


def __setup_authorization_flow_client(scope: str) -> spotipy.Spotify:
    load_dotenv()
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv('CLIENT_ID'),
            client_secret=os.getenv('CLIENT_SECRET'),
            redirect_uri=os.getenv('REDIRECT_URI'),
            scope=scope
        )
    )


def run_test_user_data():
    scope = "user-read-recently-played"
    client = __setup_authorization_flow_client(scope)
    max_limit = 50

    def calculate_unix_timestamp():
        return int(tm.time())

    recently_played_response = client.current_user_recently_played(
        limit=max_limit, after=calculate_unix_timestamp())

    songs_data = []
    different_day = False
    curr_date = datetime.now().date()
    while not different_day and recently_played_response['items']:
        for item in recently_played_response['items']:
            track_played_at = datetime.fromisoformat(item['played_at']).date()
            if curr_date != track_played_at:
                different_day = True
                break
            track_name = item['track']['name']
            track_id = item['track']['id']
            artists_names = [artist_data['name'] for artist_data in item['track']['artists']]
            all_artists = ', '.join(artists_names)
            songs_data.append(
                f"****** ({track_id}) {track_name} - {all_artists}. Played at: {item['played_at']}")

        if not different_day:
            recently_played_response = client.current_user_recently_played(
                limit=max_limit, before=recently_played_response['cursors']['after'])  # go backwards

    for song in songs_data:
        print(song)
    print(f"total songs: {len(songs_data)}")


def run_test_seeds():
    client = __setup_general_data_client()

    seed_tracks = ["6NMtzpDQBTOfJwMzgMX0zl", "2alpVcC9RxRWS1eSMGeAAP", "6ewQE1dNPv9qqlnB1CxrvM"]
    seed_artists = ["0Y5tJX1MQlPlqiwlOH1tJY", "6icQOAFXDZKsumw3YXyusw", "5INjqkS1o8h1imAzPqGZBb"]
    seed_genres = ["melodic rap", "neo-psychedelic", "trip-hop", "psych-rock", "rap"]

    # 6NMtzpDQBTOfJwMzgMX0zl - skeletons - 0Y5tJX1MQlPlqiwlOH1tJY - Travis Scott
    # ['hip hop', 'rap', 'slap house']

    # 2alpVcC9RxRWS1eSMGeAAP - THE zone~ - 6icQOAFXDZKsumw3YXyusw - Lil Yachy (add some noise)
    # ['atl hip hop', 'melodic rap', 'rap', 'trap'] 

    # 6ewQE1dNPv9qqlnB1CxrvM - Mind Mischief - 5INjqkS1o8h1imAzPqGZBb - Tame Impala (add more noise)
    # ['australian psych', 'modern rock', 'neo-psychedelic', 'rock']

    # 5 seeds between artists + genres + tracks
    recommendations = client.recommendations(
        # seed_artists=[seed_artists],
        seed_genres=[seed_genres[0], seed_genres[2]],
        seed_tracks=[seed_tracks[0], seed_tracks[1]]
    )

    for track in recommendations['tracks']:
        track_name = track['name']
        artists = []
        for artist in track['artists']:
            artists.append(artist['name'])
        print(f"********** song: {track_name} - {', '.join(artists)}")
