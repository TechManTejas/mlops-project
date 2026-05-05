from pathlib import Path
import logging

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODELS_ROOT = PROJECT_ROOT / "models" / "parking"
MODEL_CONFIG_PATH = PROJECT_ROOT / "config" / "model_config.yaml"
SUPPORTED_MODELS = {"yolov8", "yolov11"}


def get_model_path(model_name: str) -> Path:
    if model_name not in SUPPORTED_MODELS:
        raise ValueError(f"Unsupported model '{model_name}'. Use one of: {sorted(SUPPORTED_MODELS)}")
    return MODELS_ROOT / model_name / "model.pt"


def ensure_model_exists(model_name: str) -> Path:
    model_path = get_model_path(model_name)
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}. Run `dvc pull` before starting the service."
        )
    return model_path


def get_active_model_name() -> str:
    if not MODEL_CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing model config: {MODEL_CONFIG_PATH}")

    with MODEL_CONFIG_PATH.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    model_name = data.get("model", {}).get("name")
    if model_name not in SUPPORTED_MODELS:
        raise ValueError(
            f"Invalid model name '{model_name}' in {MODEL_CONFIG_PATH}. "
            f"Use one of: {sorted(SUPPORTED_MODELS)}"
        )
    
    logging.info(f"Loading model: {model_name}")
    return model_name

