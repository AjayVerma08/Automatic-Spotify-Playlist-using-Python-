# Top 100 Billboard Song
# Adds them to your spotify playlist
import requests
from os import environ
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
from pprint import pprint
URL = "https://www.billboard.com/charts/hot-100/"
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}
date = input("Which year do you want to travel to? Type the date in YYYY-MM-DD Format: ")

response = requests.post(url=f"{URL}{date}/", headers=header)
content = response.text

soup = BeautifulSoup(content, "html.parser")
songs = soup.find_all(name="h3", class_="a-no-trucate")
artists = soup.find_all(name="span", class_="a-no-trucate")
songs_list = [song.getText(strip=True) for song in songs]
artist_list = [artist.getText(strip=True) for artist in artists]

cache_path = "Day 46 Musical Time Machine (Spotify API)/token.txt"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=environ["SPOTIFY_CLIENT_ID"],
             client_secret=environ["SPOTIFY_SECRET"],
             redirect_uri=environ["SPOTIFY_REQ_URL"],
             scope="playlist-modify-private",
            cache_path=cache_path,
            username="ajay"))
user = sp.current_user()
song_uris = []
user_id = user["id"]
year = date.split("-")[0]
for song in songs_list:
    track = sp.search(q=f"track: {song}, year: {year}", type="track")
    try:
        uri = track["tracks"]["items"][0]["uri"]
        song_uris.append(uri)

    except IndexError:
        print(f"{song} was not found and was skipped ")


create_playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard Top 100", public=False)

playlist_id = create_playlist["id"]

add_songs = sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
pprint(add_songs)