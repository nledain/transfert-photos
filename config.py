
from pathlib import Path
import shutil

extensions_photos = {".jpg", ".jpeg", ".png", ".jfif"}
extensions_videos = {".mp4", ".mov", ".avi", ".mkv"}

destination_par_defaut = Path.home() / "TransfertPhotos"

# Configuration locale facultative, non versionnée
try:
    from config_local import CHEMIN_EXIFTOOL
except ImportError:
    CHEMIN_EXIFTOOL = None


def trouver_exiftool():
    """Trouve ExifTool via la configuration locale ou le PATH."""
    if CHEMIN_EXIFTOOL:
        chemin = Path(CHEMIN_EXIFTOOL)
        if chemin.is_file():
            return str(chemin)
        return None

    return shutil.which("exiftool")
