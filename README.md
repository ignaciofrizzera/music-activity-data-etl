# Music Activity Data ETL

## ETL to keep record of my music activity from Spotify. Main goals of this project:
- Practice and learn about data engineering tools such as Airflow and AWS services related to this field.
- Monitor and visualize my music data.

## Things that came across the way
I realised that the Spotify endpoint to get [recently_played songs](https://developer.spotify.com/documentation/web-api/reference/get-recently-played) only gives the latest 50 songs, but doesn't let you go any further in time. This was not ideal, since I listen to way more than 50 songs in a single day.

## Solution
Reading about AWS services, I came across AWS: Step Functions.

Since the Spotify endpoint as it is doesn't really do what I want (get all my played songs), I decided to do two things:
- Setup an AWS: Step Function to trigger a Lambda function every 1 hour in order to get all my played songs and periodically dump them in a S3 bucket.
- Since my ETL process is very simple, I created another Step Function to run it, consisting of three Lambdas for each principal function: **Extract**, **Transform**, and **Load**. It executes three times daily: initially at 9:30 AM, then at 5:30 PM, and lastly at 11:30 PM (UTC-3). Initially, it ran only once, but to diminish the volume of high API requests within a short period, I increased the frequency at which it runs.

So my project architecture looks like this:

![Architecture](static/images/architecture.png "Architecture")

## Data being tracked
The data being tracked can be divided into two main groups. The song general data and the sections data.

> ****: many of this data was pruned due to endpoints being removed from Spotify's API.

### Song General Data
This data represents general information about a song. Here are the features used here:
- **track_id**: ID of the track from Spotify's API.
- **track_name**: Title of the track.
- **track_artist**: Artist of the track.
-  **played_at**: Time at which the song was played.
-  **explicit**: Shows if the track has explicit lyrics or not.
-  **popularity**: Track popularity according to Spotify.
-  **album**: Name of the album the track belongs to.
-  **album_cover**: URL to the album's cover.
-  **album_cover_height**: Cover's height.
-  **album_cover_width**: Cover's width.
-  **duration**: Duration of the track in seconds.

### Here's how the data for a single song looks at the end of the ETL

```json
{
   "track_id":"7LSpFCvRZZot2AlmkUzy9k",
   "track_name":"SIRENS",
   "track_artist":"Travis Scott",
   "played_at":["2023-11-28 11:40", "2023-11-28 16:30"],
   "explicit":true,
   "popularity":77,
   "album":"UTOPIA",
   "album_cover":"https:\/\/i.scdn.co\/image\/ab67616d0000b273881d8d8378cd01099babcd44",
   "album_cover_height":640,
   "album_cover_width":640,
   "duration":204.4473
}
```
## Data that could be added
- The **genre** of the song is a feature that is very useful and I'm actually not getting from the tracks.
- The **segments** of the track. Just like Sections, tracks are divided in Segments. According to Spotify: *Each segment contains a roughly conisistent sound throughout its duration.*
  
  **Segments** are really interesting because they have the *pitches* property, which can be used along the [Scriabin's sound-to-color circle of fifths](https://en.wikipedia.org/wiki/Chromesthesia#:~:text=Scriabin's%20sound%2Dto%2Dcolor%20circle%20of%20fifths&text=He%20created%20a%20system%20that,sensation%20of%20touch%20and%20taste%22.) to represent a song as a series of colors and generate cool images with them.

## Visualization
You can view a basic visualization of this ETL in my [personal web page](https://www.ignaciofrizzera.com/projects/spotify-etl).

**Future Possibilities**: The dataset created from this ETL offers extensive potential for endless visualizations and analyses.

## What I Learned
- Got a lot more familiar with the whole AWS ecosystem.
- Learned about CI/CD (Github Actions workflows).
- Integrated my CI/CD to my AWS resources (Lambda Functions), which was pretty cool and simple. Even though this was a huge leap in my Lambdas knowledge, I want to improve the way I work with Layers. In this project, I manually created my Layers and updated them from the AWS web interface. I'd like to automate this or at least do it from code or CI/CD, just as I do with my Lambdas.
- Discovered the Step-Functions service, which I found very interesting and powerful. I'd like to dig deeper in how to create and deploy them as code instead of doing it by hand with the web interface (similar to what I did with my Lambdas and my CI/CD).