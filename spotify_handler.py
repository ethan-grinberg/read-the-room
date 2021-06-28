import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import numpy as np
import progressbar

os.environ["SPOTIPY_CLIENT_ID"] = '4e8ef68ce1cd4a8c9b0e9a854f1e7ae9'
os.environ["SPOTIPY_CLIENT_SECRET"] = "1b556835bc634f718be10d11512d1eb3"
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost:7777/callback'
scopes = ['streaming', 'user-read-recently-played', 'user-read-playback-position', 'user-read-playback-state',
          'user-modify-playback-state', 'playlist-read-private', 'playlist-read-collaborative', 'user-library-read',
          'user-follow-read', 'user-top-read']


class SpotifyHandler:
    def __init__(self):
        auth_manager = SpotifyOAuth(scope=scopes)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

        # progress bar
        widgets = [' [',
                   progressbar.Timer(format='elapsed time: %(elapsed)s'),
                   '] ',
                   progressbar.Bar('*'), ' (',
                   progressbar.ETA(), ') ',
                   ]
        self.bar = progressbar.ProgressBar(max_value=200, widgets=widgets).start()
        self.progress = 0

        self.song_scores = self.get_spotify_data()
        self.song_scores = {k: self.normalize_song_score(v) for k, v in self.song_scores.items()}

    def update_progress(self):
        self.progress += 1
        if self.progress >= 200:
            self.progress = 0

        self.bar.update(self.progress)

    def get_song_score(self, song_id):
        features = self.sp.audio_features(song_id)[0]
        score = (features["danceability"]) + (features["energy"]) + (features["tempo"] / 100) + (
                    features["liveness"] + features["valence"])

        # update progress bar
        self.update_progress()
        return score

    def get_spotify_data(self):
        # get song listening info
        recent_songs = self.sp.current_user_recently_played()
        top_tracks = self.sp.current_user_top_tracks()
        saved_albums = self.sp.current_user_saved_albums()

        # get scores for all songs
        recent_song_scores = {song["track"]["id"]: self.get_song_score(song["track"]["id"]) for song in
                              recent_songs["items"]}
        top_tracks_scores = {song["id"]: self.get_song_score(song["id"]) for song in top_tracks["items"]}
        albums_scores = {song["id"]: self.get_song_score(song["id"]) for album in saved_albums["items"] for song in
                         album["album"]["tracks"]["items"]}

        return {**recent_song_scores, **top_tracks_scores, **albums_scores}

    def normalize_song_score(self, val):
        max_val = max(self.song_scores.values())
        min_val = min(self.song_scores.values())
        range_ = max_val - min_val

        # update progress bar
        self.update_progress()
        return (val - min_val) / range_

    def get_closest_score(self, value):
        lst = np.asarray(list(self.song_scores.values()))
        idx = (np.abs(lst - value)).argmin()
        return list(self.song_scores.keys())[list(self.song_scores.values()).index(lst[idx])]

    def listen_and_choose(self):
        currently_playing = self.sp.currently_playing()
        seconds_left = currently_playing["progress_ms"]
        while True:
            seconds_left = currently_playing["item"]["duration_ms"] - currently_playing["progress_ms"]
            print(seconds_left)

            # Make sure the currently playing song stays up to date
            currently_playing = self.sp.currently_playing()
