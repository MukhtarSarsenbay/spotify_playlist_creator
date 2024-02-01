import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.environ['SPOTIPY_CLIENT_ID'],
        client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
        show_dialog=True,
        cache_path="token.txt",
        username="hxehdndszs3piqhw4n2tuj87d",
    )
)
user_id = sp.current_user()["id"]
date = input("which year you would like to travel in this format YYYY-MM-DD:")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
data = response.text

soup = BeautifulSoup(data, "html.parser")
list_of = soup.select("li ul li h3")
top_100 = [song.getText().strip() for song in list_of]
print(sp.search(top_100[0]))
print(top_100)
song_uris = []
year = date.split("-")[0]
for song in top_100:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

my_playlist = sp.user_playlist_create(user=f"{user_id}", name=f"{date} Billboard 100", public=False,
                                      description="Top Tracks from back in the Dayz of Brunel")

sp.playlist_add_items(playlist_id=my_playlist['external_urls']['spotify'], items=song_uris)
