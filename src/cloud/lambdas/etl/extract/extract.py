from src.cloud.s3.RawFileRepository import RawFileRepository
from src.cloud.s3.FileType import FileType
from src.cloud.lambdas.etl.utils.SummarizedTrack import SummarizedTrack
import json

def extract():
    file_repository = RawFileRepository()
    raw_data = file_repository.get(FileType.HOURLY)
    
    # Cleanup reports data, remove repeated songs from overlapped reports (e.g., 01:00, 02:00)
    songs_data = {}
    for report in raw_data:
        for _, songs in report.items(): # <Date, List of songs>
            for song in songs:
                song_key = (song['track_id'], song['played_at'])
                songs_data[song_key] = song
    songs_data = list(songs_data.values())

    # Extract data for each song and post it.
    summarized_tracks = [SummarizedTrack(song).get_data() for song in songs_data]
    file_repository.post(FileType.UNSTRUCTURED, json.dumps(summarized_tracks))