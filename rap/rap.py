from typing import List, Tuple, Dict
from summarizer.SummarizedTrack import SummarizedTrack
import json

# Rap tracks that are similar
track_ids: List[Tuple[str, str]] = [
    # Circus Maximus - Travis Scott, Black Skinhead - Kanye West.
    ("4GL9GMX9t7Qkprvf1YighZ", "722tgOgdIbNe3BEyLnejw4"),
]

def run_similar_rap_data():
    songs: List[Tuple[Dict, Dict]] = []
    for tracks_tuple in track_ids:
        track_one, track_two = tracks_tuple
        track_one_summarized = SummarizedTrack(track_one)
        track_two_summarized = SummarizedTrack(track_two)

    songs.append((track_one_summarized.data, track_two_summarized.data))
    
    data = {'songs': songs}
    with open('rap/similar_rap_data.json', 'w') as fp:
        json.dump(data, fp, indent=3)