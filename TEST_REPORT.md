# GF-Free Proxy - Rapport de Test

**Date**: 2026-01-15
**Version**: 1.1.0 (post-audit)
**Environnement**: CT 118 (localhost)

## Corrections appliquées

| # | Correction | Status |
|---|------------|--------|
| 1 | `.gitignore` ajouté | ✅ |
| 2 | `LICENSE` MIT ajouté | ✅ |
| 3 | Échappement XML complet (`escape_xml()`) | ✅ |
| 4 | Service systemd: `User=nobody` | ✅ |
| 5 | Délai pagination (0.5s entre pages) | ✅ |
| 6 | `import asyncio` déplacé en haut | ✅ |
| 7 | URL documentation corrigée | ✅ |

## Tests effectués

### Proxy direct

| Test | Endpoint | Résultat |
|------|----------|----------|
| Health check | `/health` | ✅ 200 OK |
| Capabilities | `/api?t=caps` | ✅ XML valide, 8 catégories |
| Search movies | `/api?t=search&q=matrix` | ✅ 21 résultats |
| Search movies | `/api?t=search&q=inception` | ✅ 19 résultats |
| Search TV | `/api?t=tvsearch&q=breaking+bad` | ✅ 14 résultats |

### Prowlarr (localhost:9696)

| Test | Résultat |
|------|----------|
| Indexer configuré (ID 11) | ✅ |
| Test indexer | ✅ Pass |
| Search "matrix" | ✅ 21 résultats |
| Search "breaking bad" (TV) | ✅ 14 résultats |

### Radarr (localhost:7878)

| Test | Résultat |
|------|----------|
| Indexer synchronisé (ID 12) | ✅ |
| Test indexer | ✅ Pass |

### Sonarr (localhost:8989)

| Test | Résultat |
|------|----------|
| Indexer synchronisé (ID 12) | ✅ |
| Test indexer | ✅ Pass |
| RSS/Auto-search activé | ✅ |

## Analyse de charge serveur GF

### Topologie des requêtes

```
┌──────────┐    1 req    ┌────────────┐   1-10 req   ┌─────────┐
│ Prowlarr │ ──────────► │  GF-Free   │ ───────────► │   GF    │
│ Sonarr   │             │  Proxy     │              │   API   │
│ Radarr   │ ◄────────── │  (8888)    │ ◄─────────── │         │
└──────────┘  XML resp   └────────────┘  JSON pages  └─────────┘
                               │
                               ▼
                         ┌──────────┐
                         │  CACHE   │
                         │ (5 min)  │
                         └──────────┘
```

### Métriques observées (1h de test)

| Métrique | Valeur |
|----------|--------|
| Requêtes entrantes (proxy) | 32 |
| Requêtes sortantes (→ GF) | 50 |
| **Facteur multiplicateur** | **1.56x** |

### Patterns par type de recherche

| Type | Pages GF | Résultats |
|------|----------|-----------|
| RSS/Browse (sans query) | 6-8 | 50 |
| Search "matrix" | 2 | 21 |
| Search "avatar" | 2 | 19 |
| Cache HIT | 0 | instantané |

### Estimation usage quotidien

| Scénario | Req proxy | Req GF | Ratio |
|----------|-----------|--------|-------|
| RSS sync (toutes les 15 min) | 96 | ~400 | 4.2x |
| + 10 recherches manuelles | +10 | +20 | 2x |
| **Avec cache efficace** | 106 | **~150** | **1.4x** |

### Mesures de protection serveur GF

- ✅ Cache 5 min (évite ~70% des requêtes répétées)
- ✅ Délai 0.5s entre pages de pagination
- ✅ Arrêt dès RESULTS_LIMIT (50) atteint
- ✅ Gestion 429 avec retry + backoff 5s
- ✅ MAX_PAGES=10 (limite hard)

## Logs vérifiés

```
✓ Token GF correctement masqué dans les logs (apikey=***)
✓ Requêtes HTTP loggées avec status
✓ Filtrage 36h fonctionnel
✓ Cache actif (5 min TTL)
```

## Conclusion

**Status: PRÊT POUR PRODUCTION**

Toutes les corrections de sécurité ont été appliquées et testées. Le proxy fonctionne correctement avec la stack *arr.
