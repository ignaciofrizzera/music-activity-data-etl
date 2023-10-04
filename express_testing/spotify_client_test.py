from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
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

# All available genres

def run_test_user_data():
    scope = "user-read-recently-played"
    client = __setup_authorization_flow_client(scope)
    max_limit = 50

    def calculate_unix_timestamp():
        return int(tm.time())

    recently_played_response = client.current_user_recently_played(
        limit=max_limit, after=calculate_unix_timestamp())
    # "cursors":{
    #     "after":"1696449527808",
    #     "before":"1696449527808"
    # },
    
    # use this cursos to fetch the data for a whole day
    for item in recently_played_response['items']:
        track_name = item['track']['name']
        artists_names = [artist_data['name'] for artist_data in item['track']['artists']]
        all_artists = ', '.join(artists_names)
        print(f"****** {track_name} - {all_artists}. Played at: {item['played_at']}")

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