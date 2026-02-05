from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from database import Base

class Localisant(Base):
    __tablename__ = "localisant"

    id = Column(Integer, primary_key=True, index=True)

    idu = Column(String)
    numero = Column(String)
    feuille = Column(Integer)
    section = Column(String)
    code_departement = Column(String)
    nom_commune = Column(String)
    code_commune = Column(String)
    commune_abs = Column(String)
    code_arret = Column(String)

    geom = Column(
        Geometry(
            geometry_type="MULTIPOLYGON",
            srid=2154,
            spatial_index=True
        )
    )
