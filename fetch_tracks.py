# fetch_tracks.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

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