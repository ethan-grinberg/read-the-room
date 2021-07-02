import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import pandas as pd

from process_audio import get_loudness_last

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

        # spotify device
        self.device = self.sp.devices()["devices"][0]["id"]

        #keep track of played songs
        self.picked_songs = []
        self.MAX_REPEAT_SONGS = 5

        # read song_scores csv file for speed
        self.song_scores = pd.read_csv("Data/song_scores.csv")

    def get_song_score(self, song_id):
        # weights danceability the highest and energy next highest
        features = self.sp.audio_features(song_id)[0]
        score = (2 * features["danceability"]) + (features["energy"]) + (features["tempo"] / 100) + features[
            "liveness"] + (features["loudness"] / 100)
        return score

    def update_spotify_data_file(self):
        # get song listening info
        recent_songs = self.sp.current_user_recently_played()
        top_tracks = self.sp.current_user_top_tracks()
        saved_albums = self.sp.current_user_saved_albums()

        # get scores for all songs
        recent_song_scores = {song["track"]["id"]: self.get_song_score(song["track"]["id"]) for song in
                              recent_songs["items"]}
        recent = pd.DataFrame(recent_song_scores.values(), index=recent_song_scores.keys(), columns=["song_score"])

        top_tracks_scores = {song["id"]: self.get_song_score(song["id"]) for song in top_tracks["items"]}
        top = pd.DataFrame(top_tracks_scores.values(), index=top_tracks_scores.keys(), columns=["song_score"])

        albums_scores = {song["id"]: self.get_song_score(song["id"]) for album in saved_albums["items"] for song in
                         album["album"]["tracks"]["items"]}
        albums = pd.DataFrame(albums_scores.values(), index=albums_scores.keys(), columns=["song_score"])

        # merge song sources
        merged_songs = pd.concat([recent, top, albums])

        # normalize data
        normalized = self.normalize_song_scores(merged_songs)

        # remove duplicate songs
        normalized = normalized[~normalized.index.duplicated(keep='first')]
        normalized.index.set_names("id", inplace=True)

        # update member variable
        self.song_scores = normalized

        # Write df to file
        normalized.to_csv("Data/song_scores.csv")

    @staticmethod
    def normalize_song_scores(df):
        range_ = df.max() - df.min()
        df = df - df.min()
        df = df / range_
        return df * 100

    def get_closest_score(self, value):
        sorted_df = self.song_scores.iloc[(self.song_scores['song_score']-value).abs().argsort()]
        return sorted_df.iloc[0]

    def update_played_songs_list(self, song_id):
        self.picked_songs.append(song_id)

        self.song_scores = self.song_scores.loc[~self.song_scores.id.isin(self.picked_songs)]
        if len(self.picked_songs) >= self.MAX_REPEAT_SONGS:
            # think of better way of doing this than reloading the csv
            self.song_scores = pd.read_csv("Data/song_scores.csv")
            self.picked_songs = []

    def queue_closest_song(self, loudness_score):
        # get song closest to loudness score
        closest_song = self.get_closest_score(loudness_score)
        song_id = closest_song.id

        # queue song
        uri = self.sp.audio_features(song_id)[0]["uri"]
        self.sp.add_to_queue(device_id=self.device, uri=uri)

        # make sure to add list to not repeat
        self.update_played_songs_list(song_id)

        # print song info
        print(self.sp.audio_features(song_id))
        print("loudness score: " + str(loudness_score))
        print(self.sp.track(song_id)["name"] + " score: " + str(closest_song.song_score))
        return song_id

    def listen_and_choose(self, loudness_dur):
        picked_song = False
        picked_song_id = ""

        currently_playing = self.sp.currently_playing()
        seconds_left = currently_playing["progress_ms"]
        while True:
            seconds_left = currently_playing["item"]["duration_ms"] - currently_playing["progress_ms"]
            if (seconds_left <= (2000 * loudness_dur)) and not picked_song:
                picked_song_id = self.queue_closest_song(get_loudness_last(loudness_dur))
                picked_song = True

            if currently_playing["item"]["id"] == picked_song_id:
                picked_song = False

            # Make sure the currently playing song stays up to date
            currently_playing = self.sp.currently_playing()

