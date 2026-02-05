# Carte Cadastrale Interactive

Application web de visualisation des parcelles cadastrales sur fond OpenStreetMap.

## Fonctionnalités

### Carte interactive

- **Fond de carte** : OpenStreetMap (tiles gratuits)
- **Rendu** : Canvas Leaflet (optimisé pour de nombreux polygones)
- **Navigation** : Pan, zoom, avec rechargement automatique des parcelles

### Parcelles

- **Affichage** : Contours bleus avec remplissage semi-transparent
- **Popup au clic** : Informations détaillées (section, numéro, commune, surface)
- **Simplification automatique** : Géométries simplifiées selon le niveau de zoom

### Contrôles

- **Limite** : Nombre maximum de parcelles à charger (défaut: 2000)
- **Rechargement** : Bouton ou touche Entrée dans le champ limite

### Recherche propriétaire (MAJIC)

- **API Sogefi** : Recherche des propriétaires personnes morales
- **SIREN** : Affichage du numéro SIREN si disponible
- **Note** : Seules les personnes morales sont disponibles (pas les particuliers)

## Architecture

```
static/
├── index.html      # Application carte (HTML + CSS + JS)
└── README_MAP.md   # Cette documentation

routers/
├── parcelle.py     # API GeoJSON des parcelles
└── majic.py        # Proxy API MAJIC (propriétaires)

config.py           # Configuration (tokens, SRID, etc.)
```

## Configuration

### Coordonnées par défaut

Modifier dans `index.html` > `CONFIG` :

```javascript
const CONFIG = {
  center: [49.9, 3.6], // [latitude, longitude]
  zoom: 12,
  // ...
};
```

### Style des parcelles

```javascript
parcelleStyle: {
  color: "#0066cc",     // Couleur du contour
  weight: 2,            // Épaisseur du contour
  fillOpacity: 0.15,    // Opacité du remplissage
}
```

### API MAJIC

1. Obtenir un token sur https://www.sogefi-sig.com/geoservices-apis-wms/api-open-majic/
2. Ajouter le token dans `config.py` :

```python
MAJIC_API_TOKEN = "votre_token_ici"
```

## Utilisation

1. Démarrer l'API :

   ```bash
   uvicorn main:app --reload
   ```

2. Ouvrir dans le navigateur :
   - Carte : http://localhost:8000/map
   - API docs : http://localhost:8000/docs

## Optimisations

### Performance

- **Bounding box** : Seules les parcelles visibles sont chargées
- **Simplification** : Géométries simplifiées aux faibles zooms
- **Canvas** : Rendu Canvas au lieu de SVG
- **Index spatial** : Utilisation des index PostGIS

### Requête optimisée

```sql
-- La bbox est transformée en Lambert 93 (une seule fois)
-- au lieu de transformer chaque géométrie en WGS84
WHERE ST_Intersects(geom, ST_Transform(bbox, 2154))
```
