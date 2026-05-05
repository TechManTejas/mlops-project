# MLOps System Deployment Guide

## 🚀 Project Status: READY FOR DEPLOYMENT

### ✅ Completed Tasks
- Project cleaned and optimized
- Git repository initialized and pushed to GitHub
- All services running successfully with Docker Compose
- Comprehensive documentation created
- Production-ready Kubernetes manifests prepared

---

## 🌐 Local Testing Links

### **All Services Running Successfully**

#### 🎯 Main Application Services
- **Frontend UI**: http://localhost:5173
  - React SPA with real-time model status
  - Image upload and prediction interface
  
- **BentoML API**: http://localhost:3000
  - Main inference service
  - Health endpoints and metrics

#### 📊 Monitoring Services  
- **Prometheus**: http://localhost:9090
  - Metrics collection and querying
  - Target: `parking-detector-app:3000`
  
- **Grafana**: http://localhost:3001
  - Visualization dashboards
  - Login: `admin/admin`

### 🔍 Testing Endpoints

#### API Testing
```bash
# Health Check
curl http://localhost:3000/health

# Ready Check  
curl http://localhost:3000/ready

# Metrics Endpoint
curl http://localhost:3000/metrics

# Sample Prediction (use sample image)
curl -X POST -F "image=@sample-images/P1_2022-09-15_12-28-53-f32724.jpg" \
  http://localhost:3000/predict
```

#### Expected Response Format
```json
{
  "status": "success",
  "model_version": "yolov11", 
  "inference_time": 0.245,
  "detections": 3,
  "annotated_image_base64": "...",
  "message": "Prediction completed with 3 detections using model yolov11."
}
```

---

## 🐳 Docker Compose Commands

### Start System
```bash
docker-compose up --build -d
```

### Check Status
```bash
docker-compose ps
```

### View Logs
```bash
docker-compose logs -f
docker-compose logs -f app
docker-compose logs -f prometheus  
docker-compose logs -f grafana
```

### Stop System
```bash
docker-compose down
```

---

## ☁️ AWS EC2 Deployment Instructions

### Prerequisites
- AWS EC2 instance (t3.medium or larger)
- Docker and Docker Compose installed
- Git installed
- Security groups open for ports 80, 443, 3000, 3001, 5173

### Step 1: Launch EC2 Instance
```bash
# Launch Ubuntu 22.04 LTS
# Instance Type: t3.medium (2 vCPU, 4 GB RAM)
# Storage: 20 GB SSD
# Security Group: Open ports 80, 443, 3000, 3001, 5173
```

### Step 2: Connect and Setup
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
sudo apt install git -y

# Reconnect to apply docker group changes
exit
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### Step 3: Clone and Deploy
```bash
# Clone repository
git clone https://github.com/TechManTejas/mlops-project.git
cd mlops-project

# Build and start services
docker-compose up --build -d

# Verify deployment
docker-compose ps
```

### Step 4: Configure Nginx (Optional)
```bash
# Install Nginx for reverse proxy
sudo apt install nginx -y

# Create Nginx config
sudo tee /etc/nginx/sites-available/mlops << 'EOF'
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5173;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /prometheus {
        proxy_pass http://localhost:9090;
        proxy_set_header Host $host;
    }

    location /grafana {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/mlops /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: SSL Certificate (Optional)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 🚀 Kubernetes Deployment (k3s)

### Prerequisites
- k3s installed on EC2
- kubectl configured
- ArgoCD installed

### Quick Deploy
```bash
# Install k3s
curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644

# Install ArgoCD
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Deploy application
kubectl apply -f infra/k8s/argocd-application.yaml

# Access services
kubectl port-forward svc/parking-detector-app -n mlops 3000:3000
kubectl port-forward svc/grafana -n mlops 3001:3000
```

---

## 🔧 Configuration

### Model Switching
Edit `config/model_config.yaml`:
```yaml
model:
  name: yolov11  # Change to yolov8
```

### Environment Variables
```bash
# Production settings
export NODE_ENV=production
export LOG_LEVEL=info
```

---

## 📊 Monitoring Setup

### Grafana Dashboard Import
1. Open http://localhost:3001 (admin/admin)
2. Go to Dashboard → Import
3. Upload `monitoring/grafana-dashboard.json`
4. Select Prometheus data source

### Key Metrics to Monitor
- `parking_detector_requests_total` - Request count
- `parking_detector_request_duration_seconds` - Response time
- `parking_detector_predictions_total` - Prediction count
- Container CPU/Memory usage

---

## 🚨 Troubleshooting

### Common Issues
1. **Port conflicts**: Check if ports are already in use
2. **Docker build failures**: Verify requirements.txt and Dockerfile
3. **Model loading errors**: Check model files and ConfigMap
4. **Service not starting**: Check logs with `docker-compose logs`

### Debug Commands
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs app

# Restart services
docker-compose restart

# Clean rebuild
docker-compose down && docker-compose up --build -d
```

---

## 📈 Performance Tuning

### Docker Optimization
```yaml
# docker-compose.yml additions
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### Kubernetes Scaling
```yaml
# Horizontal scaling
replicas: 3

# Resource limits
resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

---

## 🎯 Next Steps

1. **Deploy to AWS EC2** using the instructions above
2. **Configure domain** and SSL certificates
3. **Set up monitoring alerts** in Grafana
4. **Configure CI/CD pipeline** with GitHub Actions
5. **Implement model registry** for version management

---

## 📞 Support

### GitHub Repository
- **Main Repo**: https://github.com/TechManTejas/mlops-project
- **Issues**: Report bugs and feature requests
- **Documentation**: Complete guides in repository

### Quick Links
- **Local Frontend**: http://localhost:5173
- **Local API**: http://localhost:3000  
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin)

**🎉 System is production-ready and fully functional!**
