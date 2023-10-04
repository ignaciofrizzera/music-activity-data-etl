# Music Activity Data ETL

## ETL to extract my daily music activity. Main goals of this project:
- Practice and learn about data engineering tools such as Airflow and AWS services related to this field.
- Monitor my music data (i really love music).

## What data will I track
This is yet to be defined, but the goal is to get the main song characteristics (**tempo**, **timbre**, **loudness**, **etc**) run some data transformations on it (**dimensional reduction on segments data mostly**) and use the Genius API to retrieve song lyrics and run **sentiment analysis** on them (a very basic one).

## Pivoting
The original idea of this project was to use the song characteristics I mentioned earlier, and by a hand-made dataset of similar songs, train a machine learning model that could decide if two songs sounded similar or not. This could be used in the future once this whole thing is working and I gather enough data, but I decided moving into simpler things (I believe) and go with this ETL idea.