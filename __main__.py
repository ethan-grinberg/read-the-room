from spotify_handler import SpotifyHandler


def main():
    spotify = SpotifyHandler()
    highest_song = spotify.sp.audio_features(max(spotify.song_scores, key=spotify.song_scores().get))
    print(highest_song)


if __name__ == '__main__':
    main()
