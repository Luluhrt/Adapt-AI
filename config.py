"""
Application configuration.

Centralized configuration for external APIs and application settings.
"""

# =============================================================================
# COORDINATE REFERENCE SYSTEMS
# =============================================================================

# Source SRID for cadastral data (Lambert 93 - France métropolitaine)
SOURCE_SRID = 2154

# Target SRID for web display (WGS84 - used by OpenStreetMap, Leaflet, etc.)
TARGET_SRID = 4326


# =============================================================================
# MAJIC API CONFIGURATION
# =============================================================================

# Sogefi Open MAJIC API for property owner information (personnes morales only)
# Documentation: https://geoservices.sogefi-sig.com/documentation.php?doc=api_openmajic_v2
# Get a trial token: https://www.sogefi-sig.com/geoservices-apis-wms/api-open-majic/

MAJIC_API_TOKEN = ""  # Add your API token here
MAJIC_API_BASE_URL = "https://geoservices.sogefi-sig.com/openmajic/v2"


# =============================================================================
# MAP DEFAULT SETTINGS
# =============================================================================

# Default map center (Aisne department, France)
DEFAULT_MAP_CENTER = {
    "lat": 49.9,
    "lon": 3.6,
    "zoom": 12
}

# Default parcelle query limit
DEFAULT_PARCELLE_LIMIT = 2000
