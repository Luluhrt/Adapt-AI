from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON
from database import get_db
from models.subdivision_fiscale import SubdivisionFiscale

router = APIRouter(prefix="/subdivision_fiscale", tags=["SubdivisionFiscale"])

@router.get("/")
def get_subdivision_fiscale(db: Session = Depends(get_db)):
    rows = db.query(
        SubdivisionFiscale.id,
        ST_AsGeoJSON(SubdivisionFiscale.geom).label("geometry")
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
