"""Bootstrap data ingestion and index build at container startup."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))  # or parent.parent if needed

from ingest import fetch_all_agendas
from rebuild_index import rebuild_vector_index

# Run ingestion and index build at startup
fetch_all_agendas(max_agendas=None)
rebuild_vector_index()
