from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON
from database import get_db
from models.commune import Commune

router = APIRouter(prefix="/commune", tags=["Commune"])

@router.get("/")
def get_commune(db: Session = Depends(get_db)):
    rows = db.query(
        Commune.id,
        ST_AsGeoJSON(Commune.geom).label("geometry")
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
