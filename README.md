# Music Activity Data ETL

## ETL to keep record of my music activity from Spotify. Main goals of this project:
- Practice and learn about data engineering tools such as Airflow and AWS services related to this field.
- Monitor and visualize my music data.

## Things that came across the way
I realised that the Spotify endpoint to get recently_played songs only gives you the latest 50 songs, but doesn't let you go any further in time. This was not ideal, since I listen to way more than 50 songs in a single day.

## Solution
Reading about AWS services, I came across AWS: Step Functions.

Since the Spotify endpoint as it is doesn't really do what I want (get all my played songs), I decided to do two things:
- Setup an AWS: Step Function to trigger a Lambda function every 1 hour in order to get all my played songs and periodically dump them in a S3 bucket.
- Since my ETL is simple, I decided to make another Step Function to run it, composed of 3 Lambdas, one for each main function, **Extract**, **Transform** and **Load**. This Step Function runs daily.

So my project architecture looks like this:
![Architecture](static/images/architecture.png "Architecture")

## Data being tracked
Add 


## Pivoting
The original idea of this project was to use the song characteristics I mentioned earlier, and by a hand-made dataset of similar songs, train a machine learning model that could decide if two songs sounded similar or not. This could be used in the future once this whole thing is working and I gather enough data, but I decided moving into simpler things (I believe) and go with this ETL idea.