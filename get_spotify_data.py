import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import numpy as np

scopes = ['streaming', 'user-read-recently-played', 'user-read-playback-position', 'user-read-playback-state', 'user-modify-playback-state', 'playlist-read-private', 'playlist-read-collaborative', 'user-library-read', 'user-follow-read', 'user-top-read']


# authorize
auth_manager = SpotifyOAuth(scope=scopes)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_song_score(song_id):
    features = sp.audio_features(song_id)[0]
    score = (features["danceability"]) + (features["energy"]) + (features["tempo"] / 100) + (
            features["liveness"] + features["valence"])
    return score

def get_closest_score(scores, value):
    lst = np.asarray(list(scores.values()))
    idx = (np.abs(lst - value)).argmin()

    return list(scores.keys())[list(scores.values()).index(lst[idx])]

# get song listening info
recent_songs = sp.current_user_recently_played()
# recent song scores
recent_song_scores = {song["track"]["id"]: get_song_score(song["track"]["id"]) for song in recent_songs["items"]}


# testing playing songs
song_id = get_closest_score(recent_song_scores, 5)

# song closest to target score
uri = sp.audio_features(song_id)[0]["uri"]
device = sp.devices()["devices"][0]["id"]
sp.start_playback(device_id=device, uris=[uri])


currently_playing = sp.currently_playing()
print(currently_playing["item"]["name"])
print(currently_playing["is_playing"])

seconds_left = currently_playing["progress_ms"]
while True:
    seconds_left = currently_playing["item"]["duration_ms"] - currently_playing["progress_ms"]
    print(seconds_left)

    # Make sure the currently playing song stays up to date
    currently_playing = sp.currently_playing()