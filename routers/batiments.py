from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON
from database import get_db
from models.batiments import Batiment

router = APIRouter(prefix="/batiments", tags=["Batiments"])

@router.get("/")
def get_batiments(db: Session = Depends(get_db)):
    rows = db.query(
        Batiment.id,
        ST_AsGeoJSON(Batiment.geom).label("geometry")
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
