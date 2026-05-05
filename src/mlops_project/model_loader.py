from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODELS_ROOT = PROJECT_ROOT / "models" / "parking"
SERVING_CONFIG_PATH = PROJECT_ROOT / "config" / "serving.yaml"
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


def get_active_model_version() -> str:
    if not SERVING_CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing serving config: {SERVING_CONFIG_PATH}")

    with SERVING_CONFIG_PATH.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    version = data.get("active_model_version")
    if version not in SUPPORTED_VERSIONS:
        raise ValueError(
            f"Invalid active_model_version '{version}' in {SERVING_CONFIG_PATH}. "
            f"Use one of: {sorted(SUPPORTED_VERSIONS)}"
        )
    return version

