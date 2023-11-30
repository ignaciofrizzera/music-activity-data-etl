from s3.RawFileRepository import RawFileRepository
from s3.FileType import FileType
from utils.SummarizedTrack import SummarizedTrack
from utils.SpotipyClient import SpotipyClient
import logging
import json

def extract():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    file_repository = RawFileRepository()
    raw_data = file_repository.get(FileType.HOURLY)
    
    # Cleanup reports data, remove repeated songs from overlapped reports 
    # (e.g., 01:00 and 02:00 reports probably share a lot of songs, since I'm sleeping at that time)
    songs_data = {}
    for report in raw_data:
        for _, songs in report.items(): # <Date, List of songs>
            for song in songs:
                song_key = (song['track_id'], song['played_at'])
                songs_data[song_key] = song
    songs_data = list(songs_data.values())

    # Extract data for each song and post it.
    client = SpotipyClient().general_data_client()
    summarized_tracks = []
    for song in songs_data:
        try:
            summarized_tracks.append(SummarizedTrack(client, song).get_data())
        except Exception as e:
            logger.exception(f"song_id: {song}, couldnt be summarized, err: {str(e)}")

    file_repository.post(FileType.UNSTRUCTURED, json.dumps(summarized_tracks))

def lambda_handler(event, context):
    extract()