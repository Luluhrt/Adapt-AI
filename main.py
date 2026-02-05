"""
PostGIS Cadastral API - Main Application

A FastAPI application serving French cadastral data (Parcellaire Express)
from a PostGIS database with an interactive web map interface.

Run with: uvicorn main:app --reload
Access map at: http://localhost:8000/map
API docs at: http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

# Import routers
from routers import (
    batiments,
    borne_limite_propriete,
    commune,
    emprise,
    feuille,
    localisant,
    parcelle,
    spatial_ref_sys,
    subdivision_fiscale,
)

# =============================================================================
# APPLICATION SETUP
# =============================================================================

app = FastAPI(
    title="PostGIS Cadastral API",
    description="API for French cadastral data (Parcellaire Express) with PostGIS",
    version="1.0.0",
)


# =============================================================================
# ROUTER REGISTRATION
# =============================================================================

# Cadastral data routers
app.include_router(parcelle.router)
app.include_router(batiments.router)
app.include_router(commune.router)
app.include_router(feuille.router)
app.include_router(subdivision_fiscale.router)
app.include_router(localisant.router)
app.include_router(borne_limite_propriete.router)
app.include_router(emprise.router)

# Reference data
app.include_router(spatial_ref_sys.router)


# =============================================================================
# STATIC FILES
# =============================================================================

# Serve static files (HTML, CSS, JS) from the 'static' folder
app.mount("/static", StaticFiles(directory="static"), name="static")


# =============================================================================
# ROOT ENDPOINTS
# =============================================================================

@app.get("/", tags=["Root"])
def root():
    """
    API root endpoint.
    
    Returns basic API information and links to documentation.
    """
    return {
        "name": "PostGIS Cadastral API",
        "version": "1.0.0",
        "docs": "/docs",
        "map": "/map",
        "endpoints": {
            "parcelle": "/parcelle/",
            "batiments": "/batiments/",
            "commune": "/commune/",
            "feuille": "/feuille/",
        }
    }


@app.get("/map", tags=["Root"])
def map_page():
    """
    Redirect to the interactive cadastral map.
    
    The map displays parcelles on an OpenStreetMap base layer using Leaflet.
    """
    return RedirectResponse(url="/static/index.html")
