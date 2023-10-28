# Music Activity Data ETL

## ETL to extract my daily music activity. Main goals of this project:
- Practice and learn about data engineering tools such as Airflow and AWS services related to this field.
- Monitor my music data (i really love music).

## What data will I track
This is yet to be defined, but the goal is to get the main song characteristics (**tempo**, **timbre**, **loudness**, **etc**) run some data transformations on it (**dimensional reduction on segments data mostly**) and use the Genius API to retrieve song lyrics and run **sentiment analysis** on them (a very basic one).

## Things that came across the way
I realised that the Spotify endpoint to get recently_played songs only gives you the latest 50 songs, but doesn't let you go any further in time. 

Reading about AWS services, I came across AWS: Step Functions and AWS: Glue.

Since the Spotify endpoint as it is doesn't really do what I want (get all my played songs), I decided to do two things:
- Setup an AWS: Step function to trigger a Lambda function every 1 hour (will see in the future the cost of this) in order to get all my played songs and periodically dump them in a S3 bucket.
- Since I'm on Windows and from what I've read (haven't digged much yet) Airflow isn't supported on Windows, I might setup a DAG in AWS: Glue, to learn the service and process the data I collect with my Step Function flow.

This approach will be determined by the costs of AWS, since this is a personal project.

## Pivoting
The original idea of this project was to use the song characteristics I mentioned earlier, and by a hand-made dataset of similar songs, train a machine learning model that could decide if two songs sounded similar or not. This could be used in the future once this whole thing is working and I gather enough data, but I decided moving into simpler things (I believe) and go with this ETL idea.