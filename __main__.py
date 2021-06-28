from spotify_handler import SpotifyHandler


def main():
    spotify = SpotifyHandler()
    highest_song = spotify.sp.audio_features(max(spotify.get_song_scores(), key=spotify.get_song_scores().get))
    print(highest_song)


if __name__ == '__main__':
    main()
