# MLOps System Demo Flow

## Prerequisites
- k3s cluster running
- Docker image built: `mlops-parking-detector:latest`
- kubectl configured
- Git repository with latest changes

## Demo Script (5-7 minutes)

### 1. System Overview (1 minute)
```
"Today I'll demonstrate our production-ready MLOps system for parking detection.
The system features automated model switching, GitOps deployment, and comprehensive monitoring."
```

### 2. Start the System (1 minute)
```bash
# Show current Kubernetes status
kubectl get pods -n mlops

# Start services if not running
kubectl apply -f infra/k8s/

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=parking-detector -n mlops --timeout=60s

# Show running services
kubectl get pods -n mlops
```

### 3. Show Current Model (30 seconds)
```bash
# Check current model configuration
kubectl get configmap model-config -n mlops -o yaml

# Show service health
kubectl port-forward svc/parking-detector-app -n mlops 3000:3000 &
curl http://localhost:3000/health
```

### 4. Make Prediction (1 minute)
```bash
# Open frontend in browser
echo "Frontend: http://localhost:3000"
echo "Upload sample image: sample-images/P1_2022-09-15_12-28-53-f32724.jpg"

# Or use curl for demo
curl -X POST -F "image=@sample-images/P1_2022-09-15_12-28-53-f32724.jpg" \
  http://localhost:3000/predict | jq '.'
```

**Expected Output:**
```json
{
  "status": "success",
  "model_version": "yolov11",
  "inference_time": 0.245,
  "detections": 3,
  "message": "Prediction completed with 3 detections using model yolov11."
}
```

### 5. Model Switching via GitOps (2 minutes)

#### 5.1 Change Model Configuration
```bash
# Edit model config
vim config/model_config.yaml

# Change from:
# model:
#   name: yolov11

# To:
# model:
#   name: yolov8
```

#### 5.2 Commit and Push
```bash
git add config/model_config.yaml
git commit -m "Switch model from yolov11 to yolov8"
git push origin main
```

#### 5.3 Show ArgoCD Sync
```bash
# Access ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:80 &
echo "ArgoCD UI: http://localhost:8080 (admin/admin)"

# Watch sync progress
argocd app get mlops-parking-detector
```

#### 5.4 Verify Deployment Update
```bash
# Wait for redeployment
kubectl rollout status deployment/parking-detector-app -n mlops

# Check new model
curl http://localhost:3000/health
```

### 6. Test New Model (30 seconds)
```bash
# Make prediction with new model
curl -X POST -F "image=@sample-images/P1_2022-09-15_12-28-53-f32724.jpg" \
  http://localhost:3000/predict | jq '.'
```

**Expected Output:**
```json
{
  "status": "success",
  "model_version": "yolov8",
  "inference_time": 0.189,
  "detections": 2,
  "message": "Prediction completed with 2 detections using model yolov8."
}
```

### 7. Show Monitoring (30 seconds)
```bash
# Access Prometheus
kubectl port-forward svc/prometheus -n mlops 9090:9090 &
echo "Prometheus: http://localhost:9090"

# Access Grafana
kubectl port-forward svc/grafana -n mlops 3001:3000 &
echo "Grafana: http://localhost:3001 (admin/admin)"

# Show metrics
curl http://localhost:9090/api/v1/query?query=parking_detector_predictions_total
```

### 8. Key Talking Points (1 minute)

#### What We Demonstrated:
1. **Automated Deployment**: Kubernetes manifests manage all services
2. **GitOps Workflow**: ArgoCD automatically syncs Git changes to cluster
3. **Model Switching**: Configuration changes trigger automatic redeployment
4. **Health Monitoring**: Health endpoints and comprehensive metrics
5. **Production Ready**: Error handling, logging, and fallback mechanisms

#### Architecture Highlights:
- **Frontend**: React UI with real-time status updates
- **API**: BentoML service with health checks and metrics
- **Models**: Configurable YOLO models (yolov8, yolov11)
- **Monitoring**: Prometheus + Grafana stack
- **Deployment**: k3s + ArgoCD for GitOps

#### Benefits:
- **Zero Downtime**: Rolling updates during model switches
- **Observability**: Complete monitoring and logging
- **Scalability**: Kubernetes-native deployment
- **Reliability**: Health checks and error handling
- **Automation**: GitOps eliminates manual deployment steps

## Cleanup
```bash
# Stop port forwards
pkill -f "kubectl port-forward"

# Optional: Reset to original model
git checkout main -- config/model_config.yaml
git push origin main
```

## Troubleshooting

### Common Issues:
1. **Pods not starting**: Check `kubectl describe pod -n mlops`
2. **Model loading errors**: Check ConfigMap and model files
3. **ArgoCD not syncing**: Check repository access and permissions
4. **Frontend not loading**: Check port forwarding and service status

### Quick Commands:
```bash
# Check everything
kubectl get all -n mlops
kubectl logs -f deployment/parking-detector-app -n mlops

# Force sync
argocd app sync mlops-parking-detector

# Restart services
kubectl rollout restart deployment/parking-detector-app -n mlops
```
