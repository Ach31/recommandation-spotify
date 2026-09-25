# fetch_tracks.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
import requests

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


# Récupère les IDs des 10 derniers morceaux
track_ids = [item['track']['id'] for item in recent_tracks['items']]
print(track_ids)

"""
# Récupère les features audio pour ces IDs
for track_id in track_ids:
    print(track_id)
    feature = sp.audio_analysis(track_id)
    print(feature)
"""
#Pas du même mode - Big flo et Oli
track_id = '4REI5iyrSBuKNH0sIOk0Qj'
# URL de l'API miroir musicae.io (endpoint audio-features)
url = f"https://api.musicae.io/spotify-audio-features?ids={track_id}"

response = requests.get(url)
print(response.status_code)
data = response.json
print(data)
"""
data = response.json()

# Le service retourne généralement une liste d'objets si plusieurs IDs sont envoyés
features = data.get('audio_features', [])

if features:
    track_data = features[0]
    print(track_data)

# Affiche les features pour chaque morceau
print("\n📊 Features audio pour tes 10 derniers morceaux :")
for idx, (item, feature) in enumerate(zip(recent_tracks['items'], features), 1):
    track = item['track']
    artists = ', '.join([artist['name'] for artist in track['artists']])
    print(f"{idx}. {track['name']} - {artists}")
    print(f"   - Danseabilité : {feature['danceability']:.2f}")
    print(f"   - Énergie : {feature['energy']:.2f}")
    print(f"   - Tempo (BPM) : {feature['tempo']:.1f}")
    print(f"   - Speechiness (parole) : {feature['speechiness']:.2f}")
    print("---")
"""