from typing import Dict
import logging
import json

from s3.RawFileRepository import RawFileRepository
from s3.FileType import FileType
from utils.SummarizedTrack import SummarizedTrack
from utils.SpotipyClient import SpotipyClient


def extract():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_repository = RawFileRepository()
    raw_data = file_repository.get(FileType.HOURLY) # Retrieve all hourly reports from the current day.

    # Cleanup reports data, remove repeated songs from overlapped reports 
    # (e.g., 01:00 and 02:00 reports probably share a lot of songs, since I'm sleeping at that time)
    songs_data: Dict[str, Dict[str, str]] = {} # <song_id, song_metadata>
    for report in raw_data:
        for _, songs in report.items(): # <Date, List of songs>
            for song in songs:
                song_id = song['track_id']
                if song_id not in songs_data:
                    song['played_at'] = set([song['played_at']])
                    songs_data[song_id] = song
                else:
                    songs_data.get(song_id)['played_at'].add(song['played_at'])

    songs_data = list(songs_data.values())

    # Extract data for each song and post it.
    client = SpotipyClient.general_data_client()
    summarized_tracks = []
    for song in songs_data:
        song['played_at'] = list(song['played_at'])
        try:
            summarized_tracks.append(SummarizedTrack(client, song).get_data())
        except Exception as e:
            logger.exception(f"song_id: {song}, couldn't be summarized, err: {str(e)}")

    if summarized_tracks:
        file_repository.post(FileType.UNSTRUCTURED, json.dumps(summarized_tracks))


def lambda_handler(event, context):
    extract()
