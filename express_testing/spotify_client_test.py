from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os

def __setup_client() -> spotipy.Spotify:
    load_dotenv()
    return spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET')
        )
    )

# All available genres
"""
{
   "genres":[
      "acoustic",
      "afrobeat",
      "alt-rock",
      "alternative",
      "ambient",
      "anime",
      "black-metal",
      "bluegrass",
      "blues",
      "bossanova",
      "brazil",
      "breakbeat",
      "british",
      "cantopop",
      "chicago-house",
      "children",
      "chill",
      "classical",
      "club",
      "comedy",
      "country",
      "dance",
      "dancehall",
      "death-metal",
      "deep-house",
      "detroit-techno",
      "disco",
      "disney",
      "drum-and-bass",
      "dub",
      "dubstep",
      "edm",
      "electro",
      "electronic",
      "emo",
      "folk",
      "forro",
      "french",
      "funk",
      "garage",
      "german",
      "gospel",
      "goth",
      "grindcore",
      "groove",
      "grunge",
      "guitar",
      "happy",
      "hard-rock",
      "hardcore",
      "hardstyle",
      "heavy-metal",
      "hip-hop",
      "holidays",
      "honky-tonk",
      "house",
      "idm",
      "indian",
      "indie",
      "indie-pop",
      "industrial",
      "iranian",
      "j-dance",
      "j-idol",
      "j-pop",
      "j-rock",
      "jazz",
      "k-pop",
      "kids",
      "latin",
      "latino",
      "malay",
      "mandopop",
      "metal",
      "metal-misc",
      "metalcore",
      "minimal-techno",
      "movies",
      "mpb",
      "new-age",
      "new-release",
      "opera",
      "pagode",
      "party",
      "philippines-opm",
      "piano",
      "pop",
      "pop-film",
      "post-dubstep",
      "power-pop",
      "progressive-house",
      "psych-rock",
      "punk",
      "punk-rock",
      "r-n-b",
      "rainy-day",
      "reggae",
      "reggaeton",
      "road-trip",
      "rock",
      "rock-n-roll",
      "rockabilly",
      "romance",
      "sad",
      "salsa",
      "samba",
      "sertanejo",
      "show-tunes",
      "singer-songwriter",
      "ska",
      "sleep",
      "songwriter",
      "soul",
      "soundtracks",
      "spanish",
      "study",
      "summer",
      "swedish",
      "synth-pop",
      "tango",
      "techno",
      "trance",
      "trip-hop",
      "turkish",
      "work-out",
      "world-music"
   ]
}
"""


def run_test():
    client = __setup_client()

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