"""
Parcelle (cadastral parcel) router.

Provides endpoints to query cadastral parcels with support for:
- Bounding box filtering (spatial queries)
- Geometry simplification (for performance at low zoom levels)
- Result limiting (to prevent browser overload)
"""

import json
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON

from database import get_db
from models.parcelle import Parcelle
from config import SOURCE_SRID, TARGET_SRID

# =============================================================================
# ROUTER SETUP
# =============================================================================

router = APIRouter(
    prefix="/parcelle",
    tags=["Parcelle"],
)


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.get("/")
def get_parcelles(
    db: Session = Depends(get_db),
    # Pagination
    limit: Optional[int] = Query(
        None,
        description="Maximum number of parcelles to return",
        ge=1,
        le=10000
    ),
    # Bounding box filter (WGS84 coordinates)
    xmin: Optional[float] = Query(None, description="Bounding box min longitude (WGS84)"),
    ymin: Optional[float] = Query(None, description="Bounding box min latitude (WGS84)"),
    xmax: Optional[float] = Query(None, description="Bounding box max longitude (WGS84)"),
    ymax: Optional[float] = Query(None, description="Bounding box max latitude (WGS84)"),
    # Performance options
    simplify: Optional[float] = Query(
        None,
        description="Geometry simplification tolerance in meters (e.g., 5 for zoom 14, 20 for zoom 12)"
    ),
):
    """
    Get cadastral parcels as GeoJSON FeatureCollection.
    
    Supports spatial filtering by bounding box and geometry simplification
    for better performance when displaying many parcels at low zoom levels.
    
    Returns:
        GeoJSON FeatureCollection with parcelle geometries and properties
    """
    
    # -------------------------------------------------------------------------
    # Build geometry expression
    # -------------------------------------------------------------------------
    
    if simplify and simplify > 0:
        # Simplify geometry in native SRID (meters) for accurate tolerance,
        # then transform to WGS84 for web display
        # preserve_collapsed=True keeps the topology intact
        geom_expr = func.ST_Transform(
            func.ST_Simplify(Parcelle.geom, simplify, True),
            TARGET_SRID
        )
    else:
        # No simplification, just transform to WGS84
        geom_expr = func.ST_Transform(Parcelle.geom, TARGET_SRID)
    
    # -------------------------------------------------------------------------
    # Build query with selected columns
    # -------------------------------------------------------------------------
    
    query = db.query(
        Parcelle.gid,
        Parcelle.idu,
        Parcelle.numero,
        Parcelle.section,
        Parcelle.feuille,
        Parcelle.code_dep,
        Parcelle.nom_com,
        Parcelle.contenance,
        ST_AsGeoJSON(geom_expr).label("geometry"),
    )
    
    # -------------------------------------------------------------------------
    # Apply bounding box filter (if provided)
    # -------------------------------------------------------------------------
    
    bbox_center_native = None
    
    if all(v is not None for v in [xmin, ymin, xmax, ymax]):
        # OPTIMIZATION: Transform the bounding box to native SRID once,
        # instead of transforming every geometry to WGS84.
        # This allows PostGIS to use the spatial index on the native geometry.
        bbox_native = func.ST_Transform(
            func.ST_MakeEnvelope(xmin, ymin, xmax, ymax, TARGET_SRID),
            SOURCE_SRID
        )
        query = query.filter(
            func.ST_Intersects(Parcelle.geom, bbox_native)
        )
        
        # Calculate center of bounding box for distance ordering
        center_x = (xmin + xmax) / 2
        center_y = (ymin + ymax) / 2
        bbox_center_native = func.ST_Transform(
            func.ST_SetSRID(func.ST_MakePoint(center_x, center_y), TARGET_SRID),
            SOURCE_SRID
        )
    
    # -------------------------------------------------------------------------
    # Order by distance from center (prioritize parcelles in center of screen)
    # -------------------------------------------------------------------------
    
    if bbox_center_native is not None:
        # Order by distance from parcelle centroid to screen center
        query = query.order_by(
            func.ST_Distance(func.ST_Centroid(Parcelle.geom), bbox_center_native)
        )
    
    # -------------------------------------------------------------------------
    # Apply limit
    # -------------------------------------------------------------------------
    
    if limit is not None:
        query = query.limit(limit)
    
    # -------------------------------------------------------------------------
    # Execute query and build GeoJSON response
    # -------------------------------------------------------------------------
    
    rows = query.all()
    
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": row.gid,
                "geometry": json.loads(row.geometry),
                "properties": {
                    "idu": row.idu,
                    "numero": row.numero,
                    "section": row.section,
                    "feuille": row.feuille,
                    "code_dep": row.code_dep,
                    "nom_com": row.nom_com,
                    "contenance": row.contenance,
                }
            }
            for row in rows
        ]
    }
