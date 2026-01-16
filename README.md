# GF-Free Proxy

Proxy Torznab pour Generation-Free avec filtrage automatique des torrents < 36h.

## Pourquoi ?

Generation-Free impose un délai de 36h avant de pouvoir télécharger via API/automatisation. Ce proxy filtre automatiquement les torrents trop récents pour éviter les erreurs 403.

## Installation

```bash
# Cloner le repo
git clone https://github.com/Bilou778/gf-free-proxy.git
cd gf-free-proxy

# Créer l'environnement virtuel
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# Configurer (optionnel - le token peut être passé via Prowlarr)
cp config.example.py config.py

# Lancer
./venv/bin/uvicorn main:app --host 0.0.0.0 --port 8888
```

## Installation service systemd

```bash
# Copier les fichiers
sudo mkdir -p /opt/gf-free-proxy
sudo cp -r * /opt/gf-free-proxy/
cd /opt/gf-free-proxy

# Environnement virtuel
sudo python3 -m venv venv
sudo ./venv/bin/pip install -r requirements.txt

# Service
sudo cp gf-free-proxy.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now gf-free-proxy

# Vérifier
sudo systemctl status gf-free-proxy
```

## Installation Docker (stack *arr)

Pour les utilisateurs ayant une stack *arr (Sonarr, Radarr, Prowlarr) via Docker.

### Option 1 : Image pré-construite (recommandé)

```bash
docker run -d \
  --name gf-free-proxy \
  -p 8888:8888 \
  --restart unless-stopped \
  ghcr.io/bilou778/gf-free-proxy:main
```

Ou avec docker-compose :

```yaml
services:
  gf-free-proxy:
    image: ghcr.io/bilou778/gf-free-proxy:main
    container_name: gf-free-proxy
    environment:
      - MIN_AGE_HOURS=37
    ports:
      - "8888:8888"
    restart: unless-stopped
```

### Option 2 : Build local

```bash
git clone https://github.com/Bilou778/gf-free-proxy.git
cd gf-free-proxy
docker build -t gf-free-proxy .
docker run -d --name gf-free-proxy -p 8888:8888 --restart unless-stopped gf-free-proxy
```

### Port personnalisé

Pour utiliser un port différent (ex: 9999) :

```bash
docker run -d \
  --name gf-free-proxy \
  -e LISTEN_PORT=9999 \
  -p 9999:9999 \
  --restart unless-stopped \
  ghcr.io/bilou778/gf-free-proxy:main
```

> Image basée sur Alpine Linux (~85 MB), compatible avec les autres containers LinuxServer.io de la stack *arr.

### Configuration dans Prowlarr (Docker)

Dans **Prowlarr** → Indexers → Add → Generic Torznab :
- **URL** : `http://gf-free-proxy:8888` (nom du container)
- **API Key** : Votre token Generation-Free

> Les containers Docker communiquent entre eux par leur nom. Si gf-free-proxy est sur le même réseau Docker que Prowlarr, utilisez `http://gf-free-proxy:8888`.

### Variables d'environnement

| Variable | Défaut | Description |
|----------|--------|-------------|
| `GF_BASE_URL` | `https://generation-free.org` | URL du tracker |
| `GF_API_TOKEN` | `` | Token API (optionnel si passé via Prowlarr) |
| `MIN_AGE_HOURS` | `37` | Âge minimum des torrents |
| `MAX_PAGES` | `20` | Pages max à scanner |
| `RESULTS_LIMIT` | `50` | Résultats max retournés |
| `CACHE_TTL_SECONDS` | `300` | Durée du cache (5 min) |
| `LISTEN_HOST` | `0.0.0.0` | Adresse d'écoute |
| `LISTEN_PORT` | `8888` | Port d'écoute |

## Configuration Prowlarr / Sonarr / Radarr

1. **Indexers** → Add Indexer → **Generic Torznab**
2. URL : `http://localhost:8888` (ou `http://gf-free-proxy:8888` en Docker)
3. API Key : **Votre token GF** (profil GF → Settings → API Key)
4. Cliquer **Test** puis **Save**

Les catégories (`2000` Movies, `5000` TV, etc.) sont configurables après dans Prowlarr pour filtrer les recherches, mais ne sont pas nécessaires pour la validation.

> Le token GF est passé via le champ API Key - pas besoin de le stocker dans config.py

## Test

```bash
# Capabilities
curl "http://localhost:8888/api?t=caps"

# Recherche
curl "http://localhost:8888/api?t=search&q=batman&apikey=VOTRE_TOKEN_GF"

# Health check
curl "http://localhost:8888/health"
```

## Logs

```bash
# Systemd
journalctl -u gf-free-proxy -f

# Docker
docker logs -f gf-free-proxy
```

## Licence

MIT
