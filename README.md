# song-similarity

project that aims to make a model that decides if two songs are similar or not based on different song attributes such as:
  - tempo
  - timbre
  - pitches
  - etc

also aiming to create datasets for some genres (rap, rock, dubstep) of similar known songs.


still trying to figure out most of this, so work in progress :)

# new idea (work in progress)
 - create 3-4 seeds with the /recommendations endpoint to get the "similar" songs, create a kind of ETL, so we automate the similar song hunting and don't do it by-hand
 - transform the data (mostly tempo, timbre and pitches) to make a more readable dataset
 - create a model with the songs i looked by hand? and use that model to see if the /recommendations seeded songs are similar or not (at the end of the day the model accuracy doesn't matter but the process of ETL + model to work with that data)
