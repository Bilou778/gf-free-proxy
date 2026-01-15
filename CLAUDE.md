# GF-Free Proxy - Documentation technique

## Contexte

Generation-Free applique un délai de 36h sur les téléchargements via API/automatisation. Ce proxy Torznab filtre automatiquement les torrents trop récents.

## Architecture

```
Prowlarr/Sonarr/Radarr
         │
         ▼
   GF-Free Proxy (:8888)
         │
         ├── Reçoit requête Torznab
         ├── Interroge API GF (pagination auto)
         ├── Filtre: created_at >= 36h
         ├── Cache mémoire (5 min TTL)
         │
         ▼
   Réponse XML Torznab
```

## Configuration

| Variable | Description | Défaut |
|----------|-------------|--------|
| `GF_BASE_URL` | URL du tracker | `https://generation-free.org` |
| `GF_API_TOKEN` | Token API (optionnel si passé via apikey) | `""` |
| `MIN_AGE_HOURS` | Âge minimum des torrents | `36` |
| `MAX_PAGES` | Pages max à scanner par requête | `10` |
| `RESULTS_LIMIT` | Résultats max retournés | `50` |
| `CACHE_TTL_SECONDS` | Durée du cache | `300` |

## Endpoints Torznab

| Endpoint | Description |
|----------|-------------|
| `GET /api?t=caps` | Capabilities |
| `GET /api?t=search&q=...` | Recherche générale |
| `GET /api?t=tvsearch&q=...&season=X&ep=Y` | Recherche séries |
| `GET /api?t=movie&q=...&imdbid=...` | Recherche films |
| `GET /health` | Health check JSON |

## API Key Pass-through

Le token GF peut être passé de deux façons :

1. **Via le champ API Key de l'indexer** (recommandé)
   - Plus sécurisé, pas de token en dur
   - Permet multi-utilisateurs

2. **Via `config.py`** (fallback)
   - Utilisé si aucun token dans la requête

## Mapping catégories

```python
# Torznab → GF
2000 (Movies) → [1, 16, 17, 7]  # Films, HD, 4K, Animation
5000 (TV)     → [2, 18]         # Séries, Séries HD
3000 (Audio)  → [3, 4]          # FLAC, MP3
4000 (PC)     → [5]             # Logiciels
7000 (Books)  → [6]             # E-books
```

## Dépendances

- Python 3.10+
- FastAPI
- Uvicorn
- httpx
- python-dateutil
