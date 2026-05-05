from pathlib import Path
import argparse

PROJECT_ROOT = Path(__file__).parent
MODELS_DIR = PROJECT_ROOT / "models" / "parking"


def get_model_path(version: str) -> Path:
    if version not in {"v1", "v2"}:
        raise ValueError("version must be one of: v1, v2")
    return MODELS_DIR / version / "model.onnx"


def simulate_model_load(version: str) -> Path:
    model_path = get_model_path(version)
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found: {model_path}. Run 'dvc pull' first."
        )
    print(f"[SIMULATION] Loaded model version '{version}' from: {model_path}")
    return model_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="v1", choices=["v1", "v2"])
    args = parser.parse_args()
    simulate_model_load(args.version)