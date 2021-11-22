# Read The Room
An algorithm that automatically chooses the next song to play next based on the loudness in the room. The songs are picked from your Spotify library.
## How To Use
- Get Spotify API [keys](https://developer.spotify.com/)
- clone this repository
- add your API keys to a file named `keys.env` (you first have to have the dotenv package installed). Label the keys as follows: `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, `SPOTIPY_REDIRECT_URI` (the redirect uri can just be `http://localhost:7777/callback`)
- start Spotify on your computer (where the repository is cloned) and play any song
- cd into the repository
- run `python __main__.py update` to in order to scrape your spotify library
- then run `python __main__.py play` to start automatically picking songs
