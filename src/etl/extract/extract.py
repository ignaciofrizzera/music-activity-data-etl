from src.cloud.s3.FileRepository import FileRepository
from src.utils.SummarizedTrack import SummarizedTrack
import json

def extract():
    file_repository = FileRepository()
    raw_data = file_repository.get_hourly()
    
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
    file_repository.post_unstructured(json.dumps(summarized_tracks))

    """
        We'll work with batches of data.

        TODO: the way things are right now, we might process at most 50 songs x2 times.
            ^ date n, report 00:00.
              date n-1, report 23:00.
            these two reports will probably share a lot of songs (at most 50), 
            and will be processed in two different batches, meaning we might do 50 songs x2.
            
            ^ on load() we'll drop these repeated songs, but at that point the work is already done,
            so might as well check for already processed songs in extract? but extract is supposed just
            to extract and gather data.
         
        extract -> gather all non-repeated songs, run summarized information on them -> post them.
        transform -> work with all the gathered data, work with sections data.
        load -> post all the cleaned data into s3 again, check for dates and repeated data
            from date n, n-1.
    """