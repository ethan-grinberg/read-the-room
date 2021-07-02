from spotify_handler import SpotifyHandler


def main():
    spotify = SpotifyHandler()
    # If I want to update my spotify data based on recent listening
    # spotify.update_spotify_data_file()

    # main function for picking songs
    spotify.listen_and_choose(10)


if __name__ == '__main__':
    main()
