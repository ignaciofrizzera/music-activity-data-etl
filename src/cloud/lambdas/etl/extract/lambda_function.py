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
            """
                So many unnecesary requests. Today (29/02/2024) I listened to the same song ~ 30 times (1:30 len)
                and that means I'll do 30 times the same exactly request? Improve this.
                Things to improve:
                    - requests made (main thing)
                    - repeated data (dumping the same data x30 times in the json)
                    - ^ if i'm not gonna repeat data in the json, find a way to count the times i listened
                        to the same thing
                    - ^ make 'played_at' a list, and append each played_at to the songs dict that i'll
                        probably use to stop requesting the same thing over and over
            """
            summarized_tracks.append(SummarizedTrack(client, song).get_data())
        except Exception as e:
            logger.exception(f"song_id: {song}, couldnt be summarized, err: {str(e)}")

    file_repository.post(FileType.UNSTRUCTURED, json.dumps(summarized_tracks))

def lambda_handler(event, context):
    extract()