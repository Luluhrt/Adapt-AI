from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON
from database import get_db
from models.feuille import Feuille

router = APIRouter(prefix="/feuille", tags=["Feuille"])

@router.get("/")
def get_feuille(db: Session = Depends(get_db)):
    rows = db.query(
        Feuille.id,
        ST_AsGeoJSON(Feuille.geom).label("geometry")
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
