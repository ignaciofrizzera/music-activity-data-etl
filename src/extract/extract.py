from src.cloud.s3.FileRepository import FileRepository

def extract():
    file_repository = FileRepository()
    raw_data = file_repository.get()
    
    data_by_date = {} # <Date, list of songs played that day> (has repeated songs)
    for report in raw_data:
        for date, date_songs in report.items():
            if not data_by_date.get(date):
                data_by_date[date] = []
            data_by_date[date].extend(date_songs)
    
    # There's a lot of repeated stuff in data_by_date.
    # Since in 1 hour it's very hard to listen to more than 50 songs.
    # e.g: 01:00 and 02:00 report will probably have the same data, or a lot of repeated songs.
    data = {} # <Date, List of songs played that day> (non-repeated)
    for date, total_date_songs in data_by_date.items():
        non_repeated_data = {}
        for song in total_date_songs:
            song_key = (song['track_id'], song['played_at'])
            non_repeated_data[song_key] = song
        data[date] = list(non_repeated_data.values())
    
    for date, songs in data.items():
        print(f"date: {date}, songs played: {len(songs)}, songs listing")
        for song in songs:
            print(f"******* {song}")
    
    """
        next steps ->
        * what to do with files and dates*
            - we've the songs played by date in case of overlaps, since 00:00, 01:00, 02:00 
            reports will probably overlap with date N and N-1
            - so our final dict, data, will have at most 2 different dates
            - lookout what to do with the files, in the transform step, do we give a dataframe for the
              date? or a batch of songs. -> TODO: look into this, we only transform stuff once.
        * scan songs data with our data dict we just made *
        * see what we do with segments/sections data, since those won't be the same size
            for each song -> this will be normalized, but in the transform step, not here.*
    """