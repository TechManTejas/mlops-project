# MLOps Parking Detection System

A production-ready MLOps system for parking space detection using YOLO models, featuring automated deployment, monitoring, and GitOps workflows.

## 🚀 Project Overview

This system demonstrates end-to-end MLOps capabilities for computer vision models:
- **Model Serving**: BentoML-based API with YOLOv8/YOLOv11 models
- **Frontend**: React UI with real-time status and predictions
- **Deployment**: Kubernetes (k3s) with GitOps automation
- **Monitoring**: Prometheus + Grafana observability stack
- **CI/CD**: ArgoCD for continuous deployment from Git

## 🏗️ Architecture

### System Components

```
Frontend (React) → BentoML API → YOLO Models
     ↓                ↓              ↓
   Grafana ← Prometheus ← Metrics Collection
     ↓                ↓
   Dashboard   ←   Kubernetes (k3s)
                      ↓
                 ArgoCD ← Git Repository
```

### Key Services

- **Frontend**: React SPA with real-time model status
- **API**: BentoML service with health endpoints and metrics
- **Models**: Configurable YOLOv8/YOLOv11 for parking detection
- **Monitoring**: Prometheus metrics + Grafana dashboards
- **Orchestration**: k3s lightweight Kubernetes
- **GitOps**: ArgoCD automated deployments

## 📋 Features

### Core Functionality
- ✅ **Model Switching**: Config-driven model selection (yolov8/yolov11)
- ✅ **Health Monitoring**: `/health` and `/ready` endpoints
- ✅ **Error Handling**: Graceful fallbacks and error responses
- ✅ **Metrics Collection**: Request latency, prediction counts, model versions
- ✅ **Real-time UI**: Live status updates and loading indicators

### MLOps Capabilities
- ✅ **GitOps Workflow**: ArgoCD auto-syncs Git changes to cluster
- ✅ **Zero Downtime**: Rolling updates during model switches
- ✅ **Observability**: Comprehensive monitoring and logging
- ✅ **Scalability**: Kubernetes-native deployment
- ✅ **Reliability**: Health checks and resource limits

## 🛠️ Quick Start

### Prerequisites
- Docker and Docker Compose
- k3s cluster
- kubectl configured
- Git repository access

### Local Development (Docker Compose)
```bash
# Build and start all services
docker-compose up --build

# Access services
# Frontend: http://localhost:5173
# API: http://localhost:3000
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3001 (admin/admin)
```

### Production Deployment (Kubernetes)
```bash
# Install ArgoCD
kubectl apply -f infra/k8s/argocd-install.yaml

# Deploy application via GitOps
kubectl apply -f infra/k8s/argocd-application.yaml

# Access services
kubectl port-forward svc/parking-detector-app -n mlops 3000:3000
kubectl port-forward svc/grafana -n mlops 3001:3000
```

## 📊 Model Management

### Available Models
- **YOLOv8**: Optimized for speed
- **YOLOv11**: Higher accuracy

### Model Switching
1. Edit `config/model_config.yaml`:
   ```yaml
   model:
     name: yolov11  # or yolov8
   ```
2. Commit and push to Git
3. ArgoCD automatically redeploys with new model

### Model Structure
```
models/parking/
├── yolov8/
│   ├── model.pt
│   └── model.pt.dvc
└── yolov11/
    ├── model.pt
    └── model.pt.dvc
```

## 📈 Monitoring & Observability

### Metrics Collected
- Request count by endpoint
- Prediction latency distribution
- Model version usage
- Error rates
- System resource usage

### Dashboards
- **Grafana**: Visual metrics and alerts
- **Prometheus**: Raw metrics and queries

### Health Endpoints
- `/health`: Service status and model info
- `/ready`: Readiness check for load balancers
- `/metrics`: Prometheus metrics endpoint

## 🔄 CI/CD Workflow

### GitOps Process
1. **Code Change**: Push to GitHub repository
2. **ArgoCD Detection**: Monitors repository changes
3. **Automatic Sync**: Applies Kubernetes manifests
4. **Rolling Update**: Zero-downtime deployment
5. **Health Verification**: Monitors deployment success

### Deployment Triggers
- Model configuration changes
- Kubernetes manifest updates
- Docker image updates
- Configuration changes

## 🧪 Demo Guide

See [scripts/demo_flow.md](scripts/demo_flow.md) for a complete step-by-step demonstration:
1. System startup and verification
2. Model prediction demonstration
3. Live model switching via GitOps
4. Monitoring dashboard tour
5. Troubleshooting and recovery

## 📁 Project Structure

```
mlops-project/
├── src/mlops_project/          # BentoML service
│   ├── service.py             # API endpoints and logic
│   └── model_loader.py        # Model management
├── frontend/                  # React UI
│   ├── src/
│   └── public/
├── infra/k8s/                # Kubernetes manifests
│   ├── app-*.yaml           # Application deployment
│   ├── prometheus-*.yaml     # Monitoring stack
│   ├── grafana-*.yaml        # Visualization
│   └── argocd-*.yaml        # GitOps setup
├── models/parking/            # Model storage
│   ├── yolov8/
│   └── yolov11/
├── config/                   # Configuration files
├── scripts/                  # Utility scripts
├── monitoring/               # Monitoring configs
└── sample-images/           # Test images
```

## 🔧 Configuration

### Environment Variables
- `PYTHONPATH`: Application path
- `PYTHONDONTWRITEBYTECODE`: Python optimization
- `PYTHONUNBUFFERED`: Real-time logging

### Kubernetes Resources
- **App**: 100m CPU, 256Mi memory (limits: 500m, 512Mi)
- **Prometheus**: 100m CPU, 256Mi memory (limits: 300m, 512Mi)
- **Grafana**: 50m CPU, 128Mi memory (limits: 200m, 256Mi)

## 🚨 Troubleshooting

### Common Issues
1. **Model Loading Errors**: Check ConfigMap and model files
2. **Pods Not Starting**: Verify resource limits and image availability
3. **ArgoCD Sync Issues**: Check repository access and permissions
4. **Frontend Connection**: Verify port forwarding and service status

### Debug Commands
```bash
# Check pod status
kubectl get pods -n mlops

# View logs
kubectl logs -f deployment/parking-detector-app -n mlops

# Force ArgoCD sync
argocd app sync mlops-parking-detector

# Check service health
curl http://localhost:3000/health
```

## 📚 Documentation

- [Architecture Details](ARCHITECTURE.md) - System architecture and design
- [Demo Script](scripts/demo_flow.md) - Step-by-step demonstration
- [Kubernetes Setup](infra/k8s/README.md) - Deployment instructions

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes and test
4. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎯 Key Takeaways

This project demonstrates:
- **Production MLOps**: Real-world deployment patterns
- **GitOps Automation**: Zero-touch deployment workflows
- **Observability**: Comprehensive monitoring and logging
- **Reliability**: Error handling and health checks
- **Scalability**: Kubernetes-native architecture

Perfect for learning MLOps best practices and demonstrating production-ready ML systems!
