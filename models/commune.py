from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from database import Base

class Commune(Base):
    __tablename__ = "commune"

    id = Column(Integer, primary_key=True, index=True)

    nom_commune = Column(String)
    code_departement = Column(String)
    code_insee = Column(String)

    geom = Column(
        Geometry(
            geometry_type="MULTIPOLYGON",
            srid=2154,
            spatial_index=True
        )
    )
