from src.cloud.s3.FileRepository import FileRepository
from typing import Dict, Any, List

"""
{
   "general_data":{
      "track_id":"0gpFiquPvir7e3RrM4kii9",
      "track_name":"IT G MA REMIX (feat. A$AP Ferg, Father, Dumbfoundead, Waka Flocka Flame)",
      "track_artist":"Keith Ape, A$AP Ferg, Father, Dumbfoundead, Waka Flocka Flame",
      "played_at":"2023-11-02 23:16",
      "explicit":true,
      "popularity":48,
      "album":"IT G MA REMIX (feat. A$AP Ferg, Father, Dumbfoundead, Waka Flocka Flame)",
      "album_cover":"https://i.scdn.co/image/ab67616d0000b27327188d8ebcb1dbf5bfb9b8c1",
      "album_cover_height":640,
      "album_cover_width":640,
      "duration":300.0,
      "loudness":-4.206,
      "tempo":102.076,
      "key":1,
      "time_signature":4,
      "mode":1,
      "features":{
         "acousticness":0.061,
         "danceability":0.787,
         "energy":0.743,
         "instrumentalness":0,
         "speechiness":0.0642,
         "valence":0.454
      }
   },
   "sections_data":[
      {
         "start":0.0,
         "duration":19.43177,
         "loudness":-10.51,
         "tempo":102.123,
         "key":5,
         "mode":1,
         "time_signature":4
      },
      {
         "start":19.43177,
         "duration":35.8572,
         "loudness":-3.377,
         "tempo":102.213,
         "key":5,
         "mode":1,
         "time_signature":4
      },
      {
         "start":55.28897,
         "duration":21.20138,
         "loudness":-2.106,
         "tempo":101.736,
         "key":5,
         "mode":0,
         "time_signature":4
      },
      {
         "start":76.49035,
         "duration":19.43133,
         "loudness":-2.305,
         "tempo":101.595,
         "key":6,
         "mode":1,
         "time_signature":4
      },
      {
         "start":95.92168,
         "duration":53.49018,
         "loudness":-4.847,
         "tempo":102.074,
         "key":6,
         "mode":1,
         "time_signature":4
      },
      {
         "start":149.41185,
         "duration":11.19804,
         "loudness":-4.318,
         "tempo":102.158,
         "key":10,
         "mode":0,
         "time_signature":4
      },
      {
         "start":160.6099,
         "duration":26.48171,
         "loudness":-3.883,
         "tempo":102.122,
         "key":1,
         "mode":1,
         "time_signature":4
      },
      {
         "start":187.0916,
         "duration":21.46651,
         "loudness":-4.533,
         "tempo":102.529,
         "key":10,
         "mode":0,
         "time_signature":4
      },
      {
         "start":208.5581,
         "duration":8.21807,
         "loudness":-3.838,
         "tempo":102.347,
         "key":1,
         "mode":1,
         "time_signature":4
      },
      {
         "start":216.77618,
         "duration":47.67318,
         "loudness":-4.472,
         "tempo":102.121,
         "key":10,
         "mode":0,
         "time_signature":4
      },
      {
         "start":264.44937,
         "duration":22.95618,
         "loudness":-4.241,
         "tempo":102.016,
         "key":3,
         "mode":0,
         "time_signature":4
      },
      {
         "start":287.40555,
         "duration":12.59446,
         "loudness":-17.4,
         "tempo":99.215,
         "key":1,
         "mode":1,
         "time_signature":4
      }
   ]
}
"""

def transform():
    
    def __unpack_features(song: Dict[str, Any]):
        song_features = song['general_data']['features']
        for feature_key in song_features:
            song['general_data'][feature_key] = song_features[feature_key]
        song['general_data'].pop('features')
    
    def __analyze_sections(sections: List[Dict[str, Any]]) -> Dict[str, any]:
        total_sections = len(sections)
        # Averages: "loudness", "tempo".
        # Sequences: "key".
        # TODO: time_signature, mode.
        key_sequence = ''
        duration_avg = loudness_avg = tempo_avg = 0
        for section in sections:
            duration_avg += section['duration']
            loudness_avg += section['loudness']
            tempo_avg += section['tempo']
            key_sequence += f"{str(section['key'])},"
        
        return {
            'sections': total_sections,
            'section_duration_avg': round(duration_avg / total_sections, 2),
            'key_sequence': key_sequence[:-1],
            'loudness_avg': round(loudness_avg / total_sections, 2),
            'tempo_avg': round(tempo_avg / total_sections, 2),
        }

    file_repository = FileRepository()
    data = file_repository.get_daily()
    for song in data:
        __unpack_features(song)
        new_sections_data = __analyze_sections(song['sections_data'])
