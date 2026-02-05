from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON
from database import get_db
from models.localisant import Localisant

router = APIRouter(prefix="/localisant", tags=["Localisant"])

@router.get("/")
def get_localisant(db: Session = Depends(get_db)):
    rows = db.query(
        Localisant.id,
        ST_AsGeoJSON(Localisant.geom).label("geometry")
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
