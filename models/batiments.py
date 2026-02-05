from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from database import Base

class Batiment(Base):
    __tablename__ = "batiments"

    id = Column(Integer, primary_key=True, index=True)

    type_batiment = Column(String)

    geom = Column(
        Geometry(
            geometry_type="MULTIPOLYGON",
            srid=2154,
            spatial_index=True
        )
    )
