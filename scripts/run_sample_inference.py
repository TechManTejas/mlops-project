from pathlib import Path
import argparse

from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_ROOT = PROJECT_ROOT / "models" / "parking"
SAMPLE_IMAGES_DIR = PROJECT_ROOT / "sample-images"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def get_model_path(version: str) -> Path:
    if version not in {"v1", "v2"}:
        raise ValueError("version must be one of: v1, v2")
    model_path = MODELS_ROOT / version / "model.onnx"
    if not model_path.exists():
        raise FileNotFoundError(f"Missing model: {model_path}. Run dvc pull first.")
    return model_path


def run(version: str) -> None:
    model = YOLO(str(get_model_path(version)), task="detect")
    images = sorted(SAMPLE_IMAGES_DIR.glob("*.jpg"))
    if not images:
        raise FileNotFoundError(f"No .jpg files in {SAMPLE_IMAGES_DIR}")

    run_output_dir = OUTPUT_DIR / version
    run_output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Using model version: {version}")
    print(f"Processing {len(images)} sample images...")
    for image_path in images:
        result = model(str(image_path))[0]
        save_path = run_output_dir / f"prediction_{image_path.name}"
        result.save(str(save_path))
        print(f"- {image_path.name}: boxes={len(result.boxes)} -> {save_path}")

    print(f"Done. Annotated images saved in: {run_output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", choices=["v1", "v2"], default="v1")
    args = parser.parse_args()
    run(args.version)
