# auth.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

# Portées (scopes) nécessaires pour ton projet
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

# Teste la connexion
try:
    current_user = sp.current_user()
    print("✅ Connexion réussie !")
    print(f"Bonjour, {current_user['display_name']} !")
    print(f"Ton ID utilisateur : {current_user['id']}")
except Exception as e:
    print(f"❌ Erreur de connexion : {e}")