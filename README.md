# Cadastral Map API

A FastAPI application for visualizing French cadastral data (Parcellaire Express) on an interactive web map with OpenStreetMap.

## Features

- **Interactive Map**: View cadastral parcels on an OpenStreetMap base layer
- **Spatial Queries**: Filter parcels by bounding box with optimized PostGIS queries
- **Dynamic Loading**: Parcels load automatically as you pan and zoom
- **Performance Optimizations**:
  - Geometry simplification at low zoom levels
  - Center-priority ordering (parcels near screen center load first)
  - Spatial index utilization
  - Canvas rendering for smooth display
- **Parcel Information**: Click on a parcel to view its details (section, number, commune, surface, etc.)

## Prerequisites

- **Python 3.10+**
- **PostgreSQL 14+** with **PostGIS 3+** extension
- **GDAL/OGR** (for importing shapefiles)

## Installation

### 1. Clone or download the project

Download the database backup via this link : https://drive.google.com/file/d/1UbfpTQonRpzTpsxPgYM3zM844LoaK9HC/view?usp=sharing 


### 2. Create and activate virtual environment

```powershell
# Create virtual environment
python -m venv virtenv

# Activate (Windows PowerShell)
.\virtenv\Scripts\Activate.ps1

# Activate (Windows CMD)
.\virtenv\Scripts\activate.bat

# Activate (Linux/Mac)
source virtenv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary geoalchemy2
```

### 4. Set up PostgreSQL with PostGIS

```sql
-- Connect to PostgreSQL as admin
CREATE DATABASE pci_1;

-- Connect to the new database
\c pci_1

-- Enable PostGIS extension
CREATE EXTENSION postgis;
```

### 5. Import cadastral data

#### Option A: Restore from SQL backup (if provided)

```bash
psql -h localhost -U postgres -d pci_1 -f database_backup.sql
```

Or in pgAdmin:

1. Right-click on database `pci_1`
2. Select **Restore...**
3. Choose `database_backup.sql`
4. Click **Restore**

#### Option B: Import from shapefiles

Download Parcellaire Express data from [IGN Geoservices](https://geoservices.ign.fr/parcellaire-express).

Import shapefiles using `shp2pgsql` or `ogr2ogr`:

```bash
# Using ogr2ogr (recommended)
ogr2ogr -f "PostgreSQL" PG:"host=localhost dbname=pci_1 user=postgres password=1234" "PARCELLE.shp" -nln parcelle -lco GEOMETRY_NAME=geom

# Or using shp2pgsql
shp2pgsql -s 2154 -I PARCELLE.shp parcelle | psql -h localhost -d pci_1 -U postgres
```

Repeat for other layers (BATIMENT, COMMUNE, etc.) if needed.

### 6. Configure database connection

Edit `database.py` if your PostgreSQL settings differ:

```python
DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/pci_1"
```

## Running the Application

### Start the server

```bash
uvicorn main:app --reload
```

### Access the application

| URL                         | Description                    |
| --------------------------- | ------------------------------ |
| http://localhost:8000/map   | Interactive cadastral map      |
| http://localhost:8000/docs  | API documentation (Swagger UI) |
| http://localhost:8000/redoc | API documentation (ReDoc)      |

## Project Structure

```
Adapt_AI/
├── main.py              # FastAPI application entry point
├── database.py          # Database connection and session management
├── config.py            # Configuration (SRID, API tokens, etc.)
├── models/              # SQLAlchemy ORM models
│   ├── parcelle.py      # Cadastral parcel model
│   ├── batiments.py     # Buildings model
│   ├── commune.py       # Commune model
│   └── ...
├── routers/             # API route handlers
│   ├── parcelle.py      # Parcel endpoints (main)
│   ├── batiments.py     # Buildings endpoints
│   └── ...
├── static/              # Static web files
│   ├── index.html       # Interactive map application
│   └── README_MAP.md    # Map documentation
└── virt/                # Python virtual environment
```

## API Endpoints

### Parcels

```
GET /parcelle/
```

Query parameters:
| Parameter | Type | Description |
|-----------|------|-------------|
| `xmin` | float | Bounding box min longitude (WGS84) |
| `ymin` | float | Bounding box min latitude (WGS84) |
| `xmax` | float | Bounding box max longitude (WGS84) |
| `ymax` | float | Bounding box max latitude (WGS84) |
| `limit` | int | Maximum number of parcels (1-10000) |
| `simplify` | float | Geometry simplification in meters |

Example:

```
GET /parcelle/?xmin=3.5&ymin=49.8&xmax=3.7&ymax=50.0&limit=1000&simplify=5
```

Response: GeoJSON FeatureCollection

### Other endpoints

- `GET /batiments/` - Buildings
- `GET /commune/` - Communes
- `GET /feuille/` - Cadastral sheets
- `GET /` - API information

## Configuration

### `config.py`

```python
# Coordinate Reference Systems
SOURCE_SRID = 2154  # Lambert 93 (source data)
TARGET_SRID = 4326  # WGS84 (web display)

# Map defaults
DEFAULT_MAP_CENTER = {"lat": 49.9, "lon": 3.6, "zoom": 12}
DEFAULT_PARCELLE_LIMIT = 2000
```

### `database.py`

```python
DATABASE_URL = "postgresql+psycopg2://user:password@host:port/database"
```

## Usage Tips

### Map Controls

- **Pan**: Click and drag
- **Zoom**: Scroll wheel or +/- buttons
- **Parcel info**: Click on a parcel
- **Limit**: Adjust the number input in top-right corner
- **Reload**: Click "Recharger" or press Enter in limit field

### Performance

- At low zoom levels, geometries are automatically simplified
- Parcels are ordered by distance from screen center
- Default limit is 2000 parcels per view

## Troubleshooting

### "column does not exist" error

Your database column names may differ. Check actual columns:

```sql
SELECT column_name FROM information_schema.columns WHERE table_name = 'parcelle';
```

Then update `models/parcelle.py` to match.

### Parcels don't appear

1. Check database connection in `database.py`
2. Verify data was imported: `SELECT COUNT(*) FROM parcelle;`
3. Check browser console for JavaScript errors
4. Verify SRID: data should be in EPSG:2154 (Lambert 93)

### Slow loading

- Reduce the limit (e.g., 500 instead of 2000)
- Zoom in to reduce the number of parcels
- Ensure spatial index exists: `CREATE INDEX ON parcelle USING GIST (geom);`

## License

This project uses open data from IGN (Institut National de l'Information Géographique et Forestière).

## Author

Developed as part of an internship project.


