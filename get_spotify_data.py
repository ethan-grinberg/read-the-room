import random

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import numpy as np

os.environ["SPOTIPY_CLIENT_ID"] = '4e8ef68ce1cd4a8c9b0e9a854f1e7ae9'
os.environ["SPOTIPY_CLIENT_SECRET"] = "1b556835bc634f718be10d11512d1eb3"
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost:7777/callback'
scopes = ['streaming', 'user-read-recently-played', 'user-read-playback-position', 'user-read-playback-state', 'user-modify-playback-state']

def get_song_score(song_id):
    features = sp.audio_features(song_id)[0]
    score = (features["danceability"]) * (features["energy"]) * (features["tempo"] / 100)
    return round(score, 1)

# authorize
auth_manager = SpotifyOAuth(scope=scopes)
sp = spotipy.Spotify(auth_manager=auth_manager)

# get happy scores for all recent songs
songs = sp.current_user_recently_played()
song_ids = [song["track"]["id"] for song in songs["items"]]
song_scores = {song_id: get_song_score(song_id) for song_id in song_ids}


def get_closest_score(scores, value):
    lst = np.asarray(list(scores.values()))
    idx = (np.abs(lst - value)).argmin()

    return list(scores.keys())[list(scores.values()).index(lst[idx])]


song_id = get_closest_score(song_scores, 0)
print(song_scores[song_id])

# play rand song
uri = sp.audio_features(song_id)[0]["uri"]
device = sp.devices()["devices"][0]["id"]
sp.start_playback(device_id=device, uris=[uri])





