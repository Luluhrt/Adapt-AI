from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from database import Base

class BorneLimitePropriete(Base):
    __tablename__ = "borne_limite_propriete"

    id = Column(Integer, primary_key=True, index=True)

    id_propriete = Column(String)

    geom = Column(
        Geometry(
            geometry_type="MULTIPOLYGON",
            srid=2154,
            spatial_index=True
        )
    )
