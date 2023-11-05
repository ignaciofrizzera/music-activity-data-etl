from src.cloud.s3.FileRepository import FileRepository
from typing import Dict, Any, List
import json

def transform():

   def __unpack_features(song: Dict[str, Any]):
      song_features = song['general_data']['features']
      for feature_key in song_features:
         song['general_data'][feature_key] = song_features[feature_key]
      song['general_data'].pop('features')
    
   def __unpack_general_data(song: Dict[str, Any]):
      general_data = song['general_data']
      for general_data_key in general_data:
         song[general_data_key] = general_data[general_data_key]
      song.pop('general_data')
   
   def __transform_sections(sections: List[Dict[str, Any]]) -> Dict[str, Any]:
      total_sections = len(sections)
        
      start_sequence = loudness_sequence = tempo_sequence = \
            key_sequence = mode_sequence = time_signature_sequence = ''
      duration_avg = loudness_avg = tempo_avg = 0
        
      for section in sections:
         duration_avg += section['duration']
         loudness_avg += section['loudness']
         tempo_avg += section['tempo']
         start_sequence +=f"{str(section['start'])},"
         loudness_sequence += f"{str(section['loudness'])},"
         tempo_sequence += f"{str(section['tempo'])},"
         key_sequence += f"{str(section['key'])},"
         mode_sequence += f"{str(section['mode'])},"
         time_signature_sequence += f"{str(section['time_signature'])},"
        
      return {
         'sections': total_sections,
         'section_duration_avg': round(duration_avg / total_sections, 2),
         'start_sequence': start_sequence[:-1],
         'loudness_sequence': loudness_sequence[:-1],
         'tempo_sequence': tempo_sequence[:-1],
         'key_sequence': key_sequence[:-1],
         'mode_sequence': mode_sequence[:-1],
         'time_signature_sequence': time_signature_sequence[:-1],
         'loudness_avg': round(loudness_avg / total_sections, 2),
         'tempo_avg': round(tempo_avg / total_sections, 2),
      }
    
   def __transform_song(song: Dict[str, Any]):
      __unpack_features(song)
      __unpack_general_data(song)
      song.update(__transform_sections(song['sections_data']))
      song.pop('sections_data')

   file_repository = FileRepository()
   data = file_repository.get_daily()
   for song in data:
      __transform_song(song)
   
   file_repository.post_structured(json.dumps(data))