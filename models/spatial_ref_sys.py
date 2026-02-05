from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from database import Base

class SpatialRefSys(Base):
    __tablename__ = "spatial_ref_sys"

    id = Column(Integer, primary_key=True, index=True)

    auth_name = Column(String)
    auth_srid = Column(Integer)
    srtext = Column(String)
    proj4text = Column(String)
