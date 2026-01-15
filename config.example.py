# GF-Free Proxy Configuration
# Copier ce fichier vers config.py et remplir les valeurs

# === API Generation-Free ===
GF_BASE_URL = "https://generation-free.org"

# Token API GF - OPTIONNEL si passé via le champ "API Key" de Prowlarr/Sonarr/Radarr
# Si vide (""), le proxy utilisera le token passé dans les requêtes (recommandé)
# Si défini, utilisé comme fallback si aucun token n'est passé dans la requête
GF_API_TOKEN = ""  # Depuis votre profil GF → Settings → API Key (optionnel)

# === Filtrage ===
MIN_AGE_HOURS = 36      # Âge minimum des torrents (délai GF)
MAX_PAGES = 10          # Pages max à scanner par requête
RESULTS_LIMIT = 50      # Résultats max retournés par requête

# === Cache ===
CACHE_TTL_SECONDS = 300  # 5 minutes

# === Serveur ===
LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 8888

# === Catégories GF → Torznab ===
# Mapping des catégories Generation-Free vers Torznab
# Format: {gf_category_id: [torznab_category_ids]}
CATEGORY_MAP = {
    # Films
    1: [2000],      # Films → Movies
    17: [2000],     # Films 4K → Movies
    16: [2000],     # Films HD → Movies
    7: [2000],      # Animation (films) → Movies
    # Séries
    2: [5000],      # Séries → TV
    18: [5000],     # Séries HD → TV
    # Audio
    3: [3000],      # FLAC → Audio
    4: [3000],      # MP3 → Audio
    # Autres
    5: [4000],      # Logiciels → PC
    6: [7000],      # E-books → Books
}

# Mapping inverse Torznab → GF pour les recherches
TORZNAB_TO_GF = {
    2000: [1, 16, 17, 7],   # Movies → Films, Films HD, Films 4K, Animation
    2010: [1],               # Movies/Foreign
    2020: [1],               # Movies/Other
    2030: [17],              # Movies/HD
    2040: [17],              # Movies/BluRay
    2045: [17],              # Movies/UHD
    5000: [2, 18],           # TV → Séries, Séries HD
    5020: [2],               # TV/Foreign
    5030: [18],              # TV/HD
    5040: [18],              # TV/HD
    3000: [3, 4],            # Audio → FLAC, MP3
    4000: [5],               # PC → Logiciels
    7000: [6],               # Books → E-books
}
