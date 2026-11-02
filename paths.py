
from pathlib import Path


def find_project_root(start_path: Path | None = None) -> Path:
    """Find the project root without relying on a machine-specific path."""

    current = (start_path or Path.cwd()).resolve()

    for candidate in (current, *current.parents):
        if (
            (candidate / "notebooks").is_dir()
            and (candidate / "src").is_dir()
        ):
            return candidate

    raise FileNotFoundError(
        "IPL Analytics project root could not be found."
    )


PROJECT_ROOT = find_project_root()

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODEL_DIR = PROJECT_ROOT / "models"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
CONFIG_DIR = PROJECT_ROOT / "config"
