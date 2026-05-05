from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODELS_ROOT = PROJECT_ROOT / "models" / "parking"
SUPPORTED_VERSIONS = {"v1", "v2"}


def get_model_path(version: str) -> Path:
    if version not in SUPPORTED_VERSIONS:
        raise ValueError(f"Unsupported version '{version}'. Use one of: {sorted(SUPPORTED_VERSIONS)}")
    return MODELS_ROOT / version / "model.onnx"


def ensure_model_exists(version: str) -> Path:
    model_path = get_model_path(version)
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}. Run `dvc pull` before starting the service."
        )
    return model_path

