from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON
from database import get_db
from models.emprise import Emprise

router = APIRouter(prefix="/emprise", tags=["Emprise"])

@router.get("/")
def get_emprise(db: Session = Depends(get_db)):
    rows = db.query(
        Emprise.id,
        ST_AsGeoJSON(Emprise.geom).label("geometry")
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
