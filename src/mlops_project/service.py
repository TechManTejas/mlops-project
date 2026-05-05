from __future__ import annotations

import base64
from functools import lru_cache
from io import BytesIO

import bentoml
import numpy as np
import onnxruntime as ort
from PIL import Image
from ultralytics import YOLO

from .model_loader import ensure_model_exists, get_active_model_version


@lru_cache(maxsize=2)
def _load_session(version: str) -> ort.InferenceSession:
    model_path = ensure_model_exists(version)
    return ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])


@lru_cache(maxsize=2)
def _load_yolo(version: str) -> YOLO:
    model_path = ensure_model_exists(version)
    return YOLO(str(model_path), task="detect")


@bentoml.service(name="parking-detector-service")
class ParkingDetectorService:
    @bentoml.api
    def health(self) -> dict[str, str]:
        return {"status": "ok", "active_model_version": get_active_model_version()}

    @bentoml.api
    def predict(self, image: Image.Image) -> dict:
        version = get_active_model_version()
        # Keep ONNXRuntime metadata check and use YOLO runtime for bbox output.
        session = _load_session(version)
        model = _load_yolo(version)
        input_names = [item.name for item in session.get_inputs()]
        output_names = [item.name for item in session.get_outputs()]
        image_array = np.array(image)
        result = model(image_array)[0]
        plotted = result.plot()
        plotted_image = Image.fromarray(plotted)
        image_buffer = BytesIO()
        plotted_image.save(image_buffer, format="JPEG")
        annotated_image_base64 = base64.b64encode(image_buffer.getvalue()).decode("utf-8")

        return {
            "model_version": version,
            "image_shape": list(image_array.shape),
            "input_names": input_names,
            "output_names": output_names,
            "detections": int(len(result.boxes)),
            "annotated_image_base64": annotated_image_base64,
            "message": f"Output generated with model version {version}.",
        }

