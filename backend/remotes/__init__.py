"""Remote modules for external QSO services."""

# Expose individual service modules for convenience
from . import clublog, lotw, ham365, qrz

__all__ = ["clublog", "lotw", "ham365", "qrz"]
