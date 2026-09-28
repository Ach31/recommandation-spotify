# fetch_tracks.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
import requests

# 1. Obtenir un token (Client Credentials Flow)
def get_spotify_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(
        auth_url,
        data={"grant_type": "client_credentials"},
        auth=(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
    )
    auth_response.raise_for_status()
    return auth_response.json()["access_token"]
# Portées (scopes) nécessaires pour récupérer tes morceaux


SCOPE = [
    "user-read-recently-played",  # Pour récupérer ton historique récent
    "user-top-read"                # Pour récupérer tes morceaux préférés
]

# Initialise le client Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
))

# Récupère tes 10 derniers morceaux écoutés
recent_tracks = sp.current_user_recently_played(limit=10)

print("🎵 Tes 10 derniers morceaux écoutés :")
for idx, item in enumerate(recent_tracks['items'], 1):
    track = item['track']
    artists = ', '.join([artist['name'] for artist in track['artists']])
    played_at = item['played_at']  # Date et heure d'écoute
    print(f"{idx}. {track['name']} - {artists} (ID: {track['id']}) | Écoute le {played_at}")


import requests

RECCO_URL = "https://api.reccobeats.com/v1/audio-features"

def get_audio_features(spotify_ids):
    """Récupère les audio features via ReccoBeats à partir d'IDs Spotify."""
    response = requests.get(
        RECCO_URL,
        params={"ids": ",".join(spotify_ids)},
        headers={"Accept": "application/json"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    # La réponse est généralement de la forme {"content": [ ... ]}
    return data.get("content", data) if isinstance(data, dict) else data

# --- suite de ton script ---
track_ids = [item["track"]["id"] for item in recent_tracks["items"]]
track_names = {item["track"]["id"]: item["track"]["name"] for item in recent_tracks["items"]}

features = get_audio_features(track_ids)

for f in features:
    # L'objet renvoyé contient un "href" pointant vers l'URL Spotify du morceau
    spotify_id = f.get("href", "").rstrip("/").split("/")[-1]
    print(track_names.get(spotify_id, spotify_id))
    for key in ("danceability", "energy", "valence", "tempo",
                "acousticness", "instrumentalness", "liveness",
                "speechiness", "loudness"):
        print(f"  {key}: {f.get(key)}")