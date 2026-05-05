from __future__ import annotations

import base64
import logging
import time
from functools import lru_cache
from io import BytesIO

import bentoml
import numpy as np
from PIL import Image
from ultralytics import YOLO
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from .model_loader import ensure_model_exists, get_active_model_name

# Prometheus metrics
REQUEST_COUNT = Counter('parking_detector_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('parking_detector_request_duration_seconds', 'Request latency')
PREDICTION_COUNT = Counter('parking_detector_predictions_total', 'Total predictions', ['model_version'])


@lru_cache(maxsize=2)
def _load_yolo(version: str) -> YOLO:
    try:
        model_path = ensure_model_exists(version)
        model = YOLO(str(model_path), task="detect")
        logging.info(f"Successfully loaded model: {version}")
        return model
    except Exception as e:
        logging.error(f"Failed to load model {version}: {str(e)}")
        raise


@bentoml.service(name="parking-detector-service", traffic={"timeout": 60})
class ParkingDetectorService:
    def __init__(self):
        self.model_version = None
        self.model_loaded = False
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Starting service initialization...")
        try:
            self.model_version = get_active_model_name()
            logging.info(f"Active model from config: {self.model_version}")
            logging.info(f"Loading model: {self.model_version}")
            model = _load_yolo(self.model_version)
            self.model_loaded = True
            logging.info(f"Service successfully initialized with model: {self.model_version}")
        except Exception as e:
            self.model_loaded = False
            logging.error(f"Service initialization failed: {str(e)}", exc_info=True)
            logging.error(f"Model version attempted: {self.model_version}")
            # Don't raise exception, allow service to start with model_loaded=False
    
    @bentoml.api
    def health(self, dummy: str = "") -> dict[str, str]:
        REQUEST_COUNT.labels(method='POST', endpoint='/health').inc()
        return {
            "status": "ok", 
            "active_model_version": self.model_version or "unknown",
            "model_loaded": str(self.model_loaded)
        }
    
    @bentoml.api
    def ready(self, dummy: str = "") -> dict[str, str]:
        REQUEST_COUNT.labels(method='POST', endpoint='/ready').inc()
        return {
            "status": "ready" if self.model_loaded else "not_ready",
            "model_version": self.model_version or "unknown",
            "model_loaded": str(self.model_loaded)
        }
    
    
    @bentoml.api
    def predict(self, image: Image.Image) -> dict:
        start_time = time.time()
        REQUEST_COUNT.labels(method='POST', endpoint='/predict').inc()
        
        if not self.model_loaded:
            error_msg = "Model not loaded - service not ready"
            logging.error(error_msg)
            return {
                "status": "error",
                "error": error_msg,
                "model_version": self.model_version or "unknown",
                "inference_time": 0.0
            }
        
        try:
            model = _load_yolo(self.model_version)
            image_array = np.array(image)
            result = model(image_array)[0]
            plotted = result.plot()
            plotted_image = Image.fromarray(plotted)
            image_buffer = BytesIO()
            plotted_image.save(image_buffer, format="JPEG")
            annotated_image_base64 = base64.b64encode(image_buffer.getvalue()).decode("utf-8")

            inference_time = time.time() - start_time
            PREDICTION_COUNT.labels(model_version=self.model_version).inc()
            REQUEST_LATENCY.observe(inference_time)
            
            logging.info(f"Prediction completed - Model: {self.model_version}, Detections: {len(result.boxes)}, Time: {inference_time:.3f}s")

            return {
                "status": "success",
                "model_version": self.model_version,
                "inference_time": round(inference_time, 3),
                "image_shape": list(image_array.shape),
                "detections": int(len(result.boxes)),
                "annotated_image_base64": annotated_image_base64,
                "message": f"Prediction completed with {len(result.boxes)} detections using model {self.model_version}.",
            }
        except Exception as e:
            inference_time = time.time() - start_time
            error_msg = f"Prediction failed: {str(e)}"
            logging.error(f"Prediction failed - Model: {self.model_version}, Error: {str(e)}, Time: {inference_time:.3f}s")
            return {
                "status": "error",
                "error": error_msg,
                "model_version": self.model_version,
                "inference_time": round(inference_time, 3)
            }

    
