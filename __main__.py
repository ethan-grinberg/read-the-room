from spotify_handler import SpotifyHandler


def main():
    spotify = SpotifyHandler()
    highest_song = spotify.sp.audio_features(max(spotify.song_scores, key=spotify.song_scores().get))
    print(highest_song)

    # main function for picking songs
    # spotify.listen_and_choose()


if __name__ == '__main__':
    main()
