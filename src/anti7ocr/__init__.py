"""anti7ocr package."""

from .__version__ import __version__
from .api import evaluate, generate, generate_batch
from .compat import AntiOcrCompat

__all__ = [
    "__version__",
    "generate",
    "generate_batch",
    "evaluate",
    "AntiOcrCompat",
]
