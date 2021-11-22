from spotify_handler import SpotifyHandler
import sys


def main():
    spotify = SpotifyHandler()
    arg = sys.argv[1]
    if arg == "update":
         spotify.update_spotify_data_file()
    elif arg == "play":
        spotify.listen_and_choose(10)


if __name__ == '__main__':
    main()
