from src.cloud.lambdas.etl.utils.SpotipyClient import SpotipyClient
from spotipy.exceptions import SpotifyException
from typing import Dict, List, Any

"""
Some info about the data.

* Track data
    - duration: 
        Length of track in seconds.
    - loudness:
        The overall loudness of a track in decibels (dB). Loudness values are 
        averaged across the entire track and are useful for comparing relative loudness of tracks. 
        Loudness is the quality of a sound that is the primary psychological correlate 
        of physical strength (amplitude). Values typically range between -60 and 0 db
    - tempo: 
        The overall estimated tempo of a track in beats per minute (BPM). 
        In musical terminology, tempo is the speed or pace of a given piece and 
        derives directly from the average beat duration
    - key:
        The estimated overall key of the section. The values in this field ranging from 0 to 11 
        mapping to pitches using standard Pitch Class notation (E.g. 0 = C, 1 = C♯/D♭, 2 = D, 
        and so on). If no key was detected, the value is -1
    - time_signature: 
        An estimated time signature. 
        The time signature (meter) is a notational convention to specify how many beats are in 
        each bar (or measure). 
        The time signature ranges from 3 to 7 indicating time signatures of "3/4", to "7/4".
    - mode: 
        Mode indicates the modality (major or minor) of a track, 
        the type of scale from which its melodic content is derived.
        (major = 1, minor = 0)
        
* Audio features data
    - acousticness
        A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 
        1.0 represents high confidence the track is acoustic.
    - danceability
        Danceability describes how suitable a track is for dancing based on a combination 
        of musical elements including tempo, rhythm stability, beat strength, and overall regularity. 
        A value of 0.0 is least danceable and 1.0 is most danceable.
    - energy
        Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and 
        activity. Typically, energetic tracks feel fast, loud, and noisy. 
        Perceptual features contributing to this attribute include dynamic range, 
        perceived loudness, timbre, onset rate, and general entropy.
    - instrumentalness
        Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as 
        instrumental in this context. Rap or spoken word tracks are clearly "vocal". 
        The closer the instrumentalness value is to 1.0, the greater likelihood the track 
        contains no vocal content.
    - speechiness
        Speechiness detects the presence of spoken words in a track. The more exclusively 
        speech-like the recording (e.g. talk show, audio book, poetry), 
        the closer to 1.0 the attribute value.
    - valence
        A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. 
        Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), 
        while tracks with low valence sound more negative (e.g. sad, depressed, angry)
        
Sections are defined by large variations in rhythm or timbre, e.g. chorus, verse, bridge, 
guitar solo, etc. Each section contains its own descriptions of tempo, key, mode, 
time_signature, and loudness.
* Sections data
    - start
    - duration
    - loudness
    - tempo
    - key
    - mode
    - time_signature
"""

class SummarizedTrack:
    __spotify_client = SpotipyClient().general_data_client()
    
    @staticmethod
    def __get_track_data(
        track_response_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        clean_data = {
            'explicit': track_response_data['explicit'], 
            'popularity': track_response_data['popularity']
        }
        clean_data['album'] = track_response_data['album']['name']
        track_album_image = track_response_data['album']['images'][0]
        clean_data['album_cover'] = track_album_image['url']
        clean_data['album_cover_height'] = track_album_image['height']
        clean_data['album_cover_width'] = track_album_image['width']
        return clean_data

    @staticmethod
    def __get_track_audio_analysis_data(
        track_audio_analysis_response_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        track_keys_to_keep = ['duration', 'loudness', 'tempo', 'key', 'time_signature', 'mode']
        clean_data = {}
        for track_key in track_keys_to_keep:
            clean_data[track_key] = track_audio_analysis_response_data[track_key]
        return clean_data

    @staticmethod
    def __get_sections_data(
        sections_response_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        section_keys_to_keep = [
            'start', 'duration', 'loudness', 'tempo', 'key', 'mode', 'time_signature']
        clean_data = []
        for section in sections_response_data:
            clean_section_data = {}
            for section_key in section_keys_to_keep:
                clean_section_data[section_key] = section[section_key]
            clean_data.append(clean_section_data)
        return clean_data

    @staticmethod
    def __get_audio_features_data(
        audio_features_response_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        audio_features_keys_to_keep = [
            'acousticness', 'danceability', 'energy', 'instrumentalness', 'speechiness', 'valence'
        ]
        clean_audio_feature_data = {}
        for audio_feature in audio_features_response_data:
            for audio_feature_key in audio_features_keys_to_keep:
                clean_audio_feature_data[audio_feature_key] = audio_feature[audio_feature_key]
        return clean_audio_feature_data

    @staticmethod
    def __merge_overall_data(
        overall_data: Dict[str, Any], 
        features_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        overall_data['features'] = features_data
        return overall_data

    def __str__(self) -> str:
        return f"{self.data['general_data']}"
    
    def __init__(self, song_data: Dict[str, str]):
        self.data = {}

        track_id = song_data['track_id']        
        try:
            track_data = self.__spotify_client.track(track_id)
        except SpotifyException:
            track_data = None
        
        if track_data:
            self.track_id = track_id

            track_data = self.__get_track_data(track_data)
            audio_analysis = self.__spotify_client.audio_analysis(track_id)
            audio_features = self.__spotify_client.audio_features(track_id)

            overall_data = self.__get_track_audio_analysis_data(audio_analysis['track'])
            
            sections_data = self.__get_sections_data(audio_analysis['sections'])
            
            features_data = self.__get_audio_features_data(audio_features)

            overall_data = self.__merge_overall_data(overall_data, features_data)

            # don't really like this update, but we re-use data from the crawler.
            song_data.update(track_data)
            song_data.update(overall_data)

            self.data['general_data'] = song_data
            self.data['sections_data'] = sections_data
    
    def get_data(self) -> Dict[str, Any]:
        return self.data
    
    def get_general_data(self) -> Dict[str, Any]:
        return self.data['general_data']

    def get_sections_data(self) -> List[Dict[str, Any]]:
        return self.data['sections_data']