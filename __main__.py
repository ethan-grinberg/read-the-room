from spotify_handler import SpotifyHandler
from dotenv import load_dotenv
import sys
import os


def main():
    load_dotenv("keys.env")
    spotify = SpotifyHandler()
    arg = sys.argv[1]
    if arg == "update":
         spotify.update_spotify_data_file()
    elif arg == "play":
        spotify.listen_and_choose(10)


if __name__ == '__main__':
    main()
