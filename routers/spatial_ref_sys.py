from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_AsGeoJSON
from database import get_db
from models.spatial_ref_sys import SpatialRefSys

router = APIRouter(prefix="/spatial_ref_sys", tags=["SpatialRefSys"])

@router.get("/")
def get_spatial_ref_sys(db: Session = Depends(get_db)):
    rows = db.query(
        SpatialRefSys.id,
        ST_AsGeoJSON(SpatialRefSys.geom).label("geometry")
    ).all()

    return rows
