# System Architecture

## High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   BentoML API   │    │     Models      │
│   (React)       │───▶│   (Python)      │───▶│   (YOLOv8/11)  │
│   Port: 3000    │    │   Port: 3000    │    │   Configurable  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌─────────────────┐              │
         │              │   Prometheus    │              │
         │              │   Port: 9090    │              │
         │              └─────────────────┘              │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Grafana     │    │   Kubernetes    │    │     GitHub      │
│   Port: 3001    │    │   (k3s)        │    │   Repository    │
│   Dashboard     │    │   Orchestration │    │   GitOps        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                         ┌─────────────────┐
                         │     ArgoCD      │
                         │   GitOps Agent  │
                         │   Auto-Sync     │
                         └─────────────────┘
```

## Data Flow Architecture

```
┌─────────────┐    HTTP POST    ┌─────────────┐    Model Load    ┌─────────────┐
│   User      │────────────────▶│   API       │────────────────▶│   YOLO      │
│   Browser   │   /predict     │   Service    │   .pt files    │   Model     │
│             │                │             │                │             │
└─────────────┘                └─────────────┘                └─────────────┘
       │                               │                               │
       │ Image Upload                   │ Inference                     │
       │                               │                               │
       ▼                               ▼                               ▼
┌─────────────┐    Response     ┌─────────────┐    Metrics      ┌─────────────┐
│   Results   │◀────────────────│   Results   │◀──────────────│   Prometheus│
│   Display   │   JSON+Image   │   Processing│   /metrics    │   Scraping  │
│             │                │             │                │             │
└─────────────┘                └─────────────┘                └─────────────┘
```

## GitOps Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           GitHub Repository                              │
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Dockerfile │  │   K8s YAML  │  │   Config    │  │   Models    │  │
│  │             │  │   Manifests │  │   Files     │  │   (.pt)     │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Git Push
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ArgoCD                                      │
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │    Watch    │  │   Sync      │  │  Deploy     │  │   Monitor   │  │
│  │   Repo      │  │   Changes   │  │   Updates   │  │   Health    │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ kubectl apply
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Kubernetes Cluster                               │
│                              (k3s)                                       │
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │    App      │  │ Prometheus  │  │   Grafana   │  │  ConfigMaps │  │
│  │ Deployment  │  │ Deployment  │  │ Deployment  │  │             │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Service Architecture

### Core Services

1. **Frontend Service** (`parking-detector-frontend`)
   - React SPA
   - Real-time status updates
   - Image upload interface
   - Result visualization

2. **API Service** (`parking-detector-app`)
   - BentoML framework
   - RESTful endpoints
   - Model inference engine
   - Health checks & metrics

3. **Monitoring Stack**
   - **Prometheus**: Metrics collection
   - **Grafana**: Visualization dashboards

### Kubernetes Components

```
Namespace: mlops
├── ConfigMaps
│   ├── model-config (model configuration)
│   └── prometheus-config (scrape configuration)
├── Deployments
│   ├── parking-detector-app (BentoML service)
│   ├── prometheus (metrics collection)
│   └── grafana (visualization)
├── Services
│   ├── parking-detector-app (ClusterIP:3000)
│   ├── prometheus (ClusterIP:9090)
│   └── grafana (ClusterIP:3000)
└── Pods
    ├── app pods (1 replica)
    ├── prometheus pod (1 replica)
    └── grafana pod (1 replica)
```

## Model Management Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Model Storage                                    │
│                                                                         │
│  models/parking/                                                         │
│  ├── yolov8/                                                            │
│  │   ├── model.pt (YOLOv8 weights)                                      │
│  │   └── model.pt.dvc (DVC tracking)                                    │
│  └── yolov11/                                                           │
│      ├── model.pt (YOLOv11 weights)                                     │
│      └── model.pt.dvc (DVC tracking)                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ ConfigMap Mount
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Configuration Management                                │
│                                                                         │
│  config/model_config.yaml                                                │
│  model:                                                                  │
│    name: yolov11  ← Switches active model                               │
│                                                                         │
│  └── Mounted as /app/config/model_config.yaml in containers              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Monitoring & Observability Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Metrics Flow                                     │
│                                                                         │
│  Application Pods                                                        │
│  ┌─────────────┐    /metrics    ┌─────────────┐                        │
│  │   App Pod   │────────────────▶│ Prometheus  │                        │
│  │             │                │   Server    │                        │
│  │ - Request   │                │             │                        │
│  │ - Latency   │                │ - Scrapes   │                        │
│  │ - Errors    │                │ - Stores    │                        │
│  │ - Models    │                │ - Aggregates│                        │
│  └─────────────┘                └─────────────┘                        │
                                         │                               │
                                         │ Query API                       │
                                         ▼                               │
│  ┌─────────────┐    Grafana UI  ┌─────────────┐                        │
│  │   Grafana   │◀────────────────│   Dashboard │                        │
│  │   Server    │                │             │                        │
│  │ - Visualizes│                │ - Graphs    │                        │
│  │ - Alerts    │                │ - Metrics   │                        │
│  │ - Panels    │                │ - Filters   │                        │
│  └─────────────┘                └─────────────┘                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Security & Reliability Architecture

### Security Layers
- **Network**: ClusterIP services (internal communication only)
- **Authentication**: Grafana admin credentials
- **Configuration**: ConfigMaps (no secrets in plain text)

### Reliability Features
- **Health Checks**: `/health` and `/ready` endpoints
- **Fallback Handling**: Graceful error responses
- **Resource Limits**: CPU/memory constraints
- **Rolling Updates**: Zero-downtime deployments
- **Logging**: Structured logs with request tracking

### Scalability Considerations
- **Horizontal Scaling**: Replica configurations ready
- **Load Balancing**: Kubernetes service discovery
- **Resource Management**: Requests and limits defined
- **Monitoring**: Performance metrics collection
