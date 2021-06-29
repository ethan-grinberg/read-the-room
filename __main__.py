from spotify_handler import SpotifyHandler


def main():
    spotify = SpotifyHandler()
    # If I want to update my spotify data based on recent listening
    # spotify.update_spotify_data_file()
    print(spotify.sp.audio_features(spotify.get_closest_score(.12312)))

    # main function for picking songs
    # spotify.listen_and_choose()


if __name__ == '__main__':
    main()
