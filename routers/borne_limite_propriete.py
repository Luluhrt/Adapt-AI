from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON
from database import get_db
from models.borne_limite_propriete import BorneLimitePropriete

router = APIRouter(prefix="/borne_limite_propriete", tags=["BorneLimitePropriete"])

@router.get("/")
def get_borne_limite_propriete(db: Session = Depends(get_db)):
    rows = db.query(
        BorneLimitePropriete.id,
        ST_AsGeoJSON(BorneLimitePropriete.geom).label("geometry")
    ).all()

    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": r.id,
                "geometry": r.geometry,
                "properties": {}
            }
            for r in rows
        ]
    }
