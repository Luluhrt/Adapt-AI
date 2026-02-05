from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from database import Base

class Emprise(Base):
    __tablename__ = "emprise"

    id = Column(Integer, primary_key=True, index=True)

    fid = Column(Integer)

    geom = Column(
        Geometry(
            geometry_type="MULTIPOLYGON",
            srid=2154,
            spatial_index=True
        )
    )
