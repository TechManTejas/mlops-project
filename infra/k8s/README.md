# Kubernetes + GitOps Setup

## Prerequisites
- k3s cluster installed
- kubectl configured
- Docker image built and available

## Installation Steps

### 1. Install ArgoCD
```bash
kubectl apply -f infra/k8s/argocd-install.yaml
```

### 2. Wait for ArgoCD to be ready
```bash
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd
```

### 3. Get ArgoCD initial password
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### 4. Access ArgoCD UI
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:80
```
Open http://localhost:8080 in browser
Login: admin (password from step 3)

### 5. Apply ArgoCD Application
```bash
kubectl apply -f infra/k8s/argocd-application.yaml
```

## Service Access

### App Service
```bash
kubectl port-forward svc/parking-detector-app -n mlops 3000:3000
```
Access: http://localhost:3000

### Prometheus
```bash
kubectl port-forward svc/prometheus -n mlops 9090:9090
```
Access: http://localhost:9090

### Grafana
```bash
kubectl port-forward svc/grafana -n mlops 3001:3000
```
Access: http://localhost:3001
Login: admin/admin

## GitOps Workflow

1. **Model Config Changes**: Update `config/model_config.yaml` in Git
2. **Auto-sync**: ArgoCD detects changes within 3 minutes
3. **Rolling Update**: ConfigMap change triggers app redeployment
4. **Verification**: Check ArgoCD UI for sync status

## Manual Sync (if needed)
```bash
argocd app sync mlops-parking-detector
```

## Troubleshooting
```bash
# Check pod status
kubectl get pods -n mlops

# Check ArgoCD app status
argocd app get mlops-parking-detector

# Check logs
kubectl logs -f deployment/parking-detector-app -n mlops
```
