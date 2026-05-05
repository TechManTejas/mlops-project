from __future__ import annotations

from functools import lru_cache

import bentoml
import numpy as np
import onnxruntime as ort
from PIL import Image

from .model_loader import ensure_model_exists


@lru_cache(maxsize=2)
def _load_session(version: str) -> ort.InferenceSession:
    model_path = ensure_model_exists(version)
    return ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])


@bentoml.service(name="parking-detector-service")
class ParkingDetectorService:
    @bentoml.api
    def health(self) -> dict[str, str]:
        return {"status": "ok"}

    @bentoml.api
    def predict(self, image: Image.Image, version: str = "v1") -> dict:
        """
        Minimal endpoint for current step:
        - Loads model by version (v1/v2) via ONNXRuntime
        - Validates image receipt
        - Returns model/session metadata (full inference to be added next step)
        """
        session = _load_session(version)
        input_names = [item.name for item in session.get_inputs()]
        output_names = [item.name for item in session.get_outputs()]
        image_array = np.array(image)

        return {
            "model_version": version,
            "image_shape": list(image_array.shape),
            "input_names": input_names,
            "output_names": output_names,
            "message": "Model loaded successfully. Inference pipeline will be implemented next.",
        }

