from dotenv.main import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECTED_URL')
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'

class SpotifyAPI:

    def __init__(self) -> None:
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI, scope=SCOPE))

    def get_audio_features(self, unfound_tracks):

        tracks_to_get_features = []
        for track in unfound_tracks:
            track_name = track[3]
            artist = track[2]
            query = track_name + ' ' + artist
            result = self.sp.search(query, limit=5, type='track')

            found = False
            for t in result['tracks']['items']:
                if (str(t['name']).lower() in track_name.lower() and str(t['artists'][0]['name']).lower() in artist.lower() and t['id'] is not None) and not found:
                    tracks_to_get_features.append((t['id'], track))
                    found = True

        print(len(tracks_to_get_features))

        ids = [t[0] for t in tracks_to_get_features]
        batches = [ids[i:i+100] for i in range(0, len(ids), 100)]
        audio_features = []
        for batch in batches:
            audio_features.extend(self.sp.audio_features(batch))

        print(len(audio_features))

        tracks = [t[1] for t in tracks_to_get_features]
        return tracks, audio_features
    

    def get_audio_features_single_track(self, query):
    
        result = self.sp.search(query, limit=1, type='track')
    
        features = self.sp.audio_features([result['tracks']['items'][0]['id']])

        return features