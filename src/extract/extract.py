"""
    Extract will have 4 steps:
        1) Retrieve the songs listened in the whole day.
        2) For each retrieved song, gather all the data related to it from the Spotify API.
        3) For each retrieved song, gather its lyrics from the Genius API.
        4) Dump the data in s3.
"""