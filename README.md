# 🎵 Spotify Tracker – Récupération des morceaux et audio features

Première brique d'un projet de **système de recommandation musicale** en Python.

Le script `fetch_tracks.py` :

1. se connecte à ton compte Spotify (OAuth) avec [Spotipy](https://spotipy.readthedocs.io/) ;
2. récupère tes **10 derniers morceaux écoutés** ;
3. récupère les **audio features** de ces morceaux (danceability, energy, valence, tempo…) via l'API externe [ReccoBeats](https://reccobeats.com/).

> ℹ️ **Pourquoi ReccoBeats ?**
> Depuis le 27 novembre 2024, Spotify a fermé l'accès aux endpoints `audio-features` et `audio-analysis` pour les nouvelles applications. ReccoBeats est une API gratuite, sans clé, qui renvoie des métriques équivalentes à partir d'IDs Spotify.

---

## 📋 Sommaire

- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Exemple de sortie](#-exemple-de-sortie)
- [Audio features disponibles](#-audio-features-disponibles)
- [Limites connues](#-limites-connues)
- [Structure du projet](#-structure-du-projet)
- [Pistes d'évolution](#-pistes-dévolution)

---

## ✅ Prérequis

- Python **3.9+**
- Un compte Spotify
- Une application créée sur le [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

## 🚀 Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/<ton-pseudo>/<ton-repo>.git
cd <ton-repo>

# 2. (Recommandé) Créer un environnement virtuel
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install spotipy requests
```

Ou avec un fichier `requirements.txt` :

```text
spotipy
requests
```

```bash
pip install -r requirements.txt
```

## 🔧 Configuration

### 1. Créer l'application Spotify

1. Rends-toi sur le [Dashboard développeur Spotify](https://developer.spotify.com/dashboard) et clique sur **Create app**.
2. Renseigne un nom et une description.
3. Dans **Redirect URI**, ajoute par exemple : `http://127.0.0.1:8888/callback`
   (Spotify demande désormais l'adresse de loopback `127.0.0.1` plutôt que `localhost`).
4. Note ton **Client ID** et ton **Client Secret**.

### 2. Créer le fichier `config.py`

À la racine du projet, crée un fichier `config.py` :

```python
# config.py
SPOTIPY_CLIENT_ID = "ton_client_id"
SPOTIPY_CLIENT_SECRET = "ton_client_secret"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
```

> ⚠️ **Ne publie jamais tes identifiants sur GitHub.** Ajoute `config.py` (et le cache d'authentification Spotipy) à ton `.gitignore` :
>
> ```gitignore
> config.py
> .cache
> venv/
> __pycache__/
> ```

### Scopes utilisés

| Scope | Utilité |
|-------|---------|
| `user-read-recently-played` | Lire l'historique des morceaux récemment écoutés |
| `user-top-read` | Lire les morceaux et artistes les plus écoutés (prévu pour la suite) |

## ▶️ Utilisation

```bash
python fetch_tracks.py
```

Lors du **premier lancement**, ton navigateur s'ouvre pour te demander d'autoriser l'application. Après validation, Spotipy enregistre le token dans un fichier `.cache` et les lancements suivants sont automatiques.

## 📺 Exemple de sortie

```text
🎵 Tes 10 derniers morceaux écoutés :
1. Titre A - Artiste 1 (ID: 4uLU6hMCjMI75M1A2tKUQC) | Écoute le 2026-09-28T09:12:45.123Z
2. Titre B - Artiste 2, Artiste 3 (ID: 7ouMYWpwJ422jRcDASZB7P) | Écoute le 2026-09-28T09:08:10.456Z
...

Titre A
  danceability: 0.72
  energy: 0.65
  valence: 0.48
  tempo: 118.03
  acousticness: 0.12
  instrumentalness: 0.0
  liveness: 0.11
  speechiness: 0.05
  loudness: -6.4
...
```

*(Valeurs données à titre d'illustration.)*

## 🎚️ Audio features disponibles

| Feature | Description |
|---------|-------------|
| `acousticness` | Probabilité que le morceau soit acoustique |
| `danceability` | Aptitude du morceau à être dansé (rythme, régularité) |
| `energy` | Intensité et activité perçues |
| `instrumentalness` | Probabilité que le morceau ne contienne pas de voix |
| `liveness` | Présence d'un public (enregistrement live) |
| `loudness` | Volume moyen en décibels (dB) |
| `speechiness` | Présence de paroles parlées |
| `tempo` | Tempo estimé en BPM |
| `valence` | Positivité musicale (triste → joyeux) |

## ⚠️ Limites connues

- **Couverture partielle** : un morceau absent de la base ReccoBeats est simplement omis de la réponse. Le nombre de résultats peut donc être inférieur au nombre d'IDs envoyés.
- **Identifiants** : ReccoBeats renvoie son propre UUID dans le champ `id`. L'ID Spotify est extrait du champ `href` pour refaire le lien avec les morceaux d'origine.
- **Disponibilité** : ReccoBeats est un service tiers gratuit, sa disponibilité et son format de réponse peuvent évoluer. Consulte leur [site officiel](https://reccobeats.com/) pour la documentation à jour.
- **Historique limité** : l'API Spotify ne renvoie qu'un nombre limité de morceaux récents (50 maximum par appel).

## 🗂️ Structure du projet

```text
.
├── fetch_tracks.py   # Script principal
├── config.py         # Identifiants Spotify (non versionné)
├── requirements.txt  # Dépendances Python
├── .gitignore
└── README.md
```

## 🛣️ Pistes d'évolution

- [ ] Stocker les résultats dans un DataFrame `pandas` / un fichier CSV / SQLite (cache)
- [ ] Récupérer aussi les **top tracks** de l'utilisateur (`user-top-read`)
- [ ] Gérer les morceaux non trouvés par ReccoBeats (fallback sur une autre API, ex. SoundStat)
- [ ] Construire le **profil d'écoute** moyen de l'utilisateur
- [ ] Recommander des morceaux par similarité (distance cosinus sur les audio features)
- [ ] Visualiser les features (radar chart, PCA)

## 📚 Ressources

- [Documentation Spotipy](https://spotipy.readthedocs.io/)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api)
- [ReccoBeats](https://reccobeats.com/)

## 📄 Licence

Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.