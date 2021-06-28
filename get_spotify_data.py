import random

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import numpy as np

os.environ["SPOTIPY_CLIENT_ID"] = '4e8ef68ce1cd4a8c9b0e9a854f1e7ae9'
os.environ["SPOTIPY_CLIENT_SECRET"] = "1b556835bc634f718be10d11512d1eb3"
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost:7777/callback'
scopes = ['streaming', 'user-read-recently-played', 'user-read-playback-position', 'user-read-playback-state', 'user-modify-playback-state', 'playlist-read-private', 'playlist-read-collaborative', 'user-library-read', 'user-follow-read', 'user-top-read']

def get_song_score(song_id):
    features = sp.audio_features(song_id)[0]
    score = (features["danceability"]) + (features["energy"]) + (features["tempo"] / 100) + (features["liveness"])
    return round(score, 1)

# authorize
auth_manager = SpotifyOAuth(scope=scopes)
sp = spotipy.Spotify(auth_manager=auth_manager)

# get song listening info
recent_songs = sp.current_user_recently_played()
top_tracks = sp.current_user_top_tracks()
saved_albums = sp.current_user_saved_albums()

#get scores for all songs
recent_song_scores = {song["track"]["id"]: get_song_score(song["track"]["id"]) for song in recent_songs["items"]}
# top_tracks_scores = {song["id"]: get_song_score(song["id"]) for song in top_tracks["items"]}
# albums_scores = {song["id"]: get_song_score(song["id"]) for album in saved_albums["items"] for song in album["album"]["tracks"]["items"]}

#combine all songs
# song_scores = {**recent_song_scores, **top_tracks_scores, **albums_scores}


def get_closest_score(scores, value):
    lst = np.asarray(list(scores.values()))
    idx = (np.abs(lst - value)).argmin()

    return list(scores.keys())[list(scores.values()).index(lst[idx])]


song_id = get_closest_score(recent_song_scores, 0)

# song closest to target score
uri = sp.audio_features(song_id)[0]["uri"]
device = sp.devices()["devices"][0]["id"]
sp.start_playback(device_id=device, uris=[uri])


currently_playing = sp.currently_playing()
print(currently_playing["progress_ms"])
print(currently_playing["item"])
print(currently_playing["is_playing"])









