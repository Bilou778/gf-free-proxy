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

## Configuration Prowlarr / Sonarr / Radarr

1. **Indexers** → Add Indexer → **Generic Torznab**
2. URL: `http://localhost:8888`
3. API Key: **Votre token GF** (profil GF → Settings → API Key)
4. Categories: `2000` (Movies), `5000` (TV)

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
journalctl -u gf-free-proxy -f
```

## Licence

MIT
