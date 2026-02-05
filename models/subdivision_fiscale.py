from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from database import Base

class SubdivisionFiscale(Base):
    __tablename__ = "subdivision_fiscale"

    id = Column(Integer, primary_key=True, index=True)

    lettre = Column(String)
    idu_parcelle = Column(String)

    geom = Column(
        Geometry(
            geometry_type="MULTIPOLYGON",
            srid=2154,
            spatial_index=True
        )
    )
