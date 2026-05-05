# EC2 Deployment Guide

## Prerequisites

1. **EC2 Instance Requirements:**
   - Minimum: t3.medium (2 vCPU, 4 GB RAM)
   - Recommended: t3.large (2 vCPU, 8 GB RAM)
   - Storage: 20 GB SSD
   - OS: Ubuntu 20.04 LTS or later

2. **Security Group Configuration:**
   - Port 22 (SSH): Your IP address
   - Port 3000 (Backend API): 0.0.0.0/0
   - Port 5173 (Frontend): 0.0.0.0/0
   - Port 9090 (Prometheus): Your IP address (optional)
   - Port 3001 (Grafana): Your IP address (optional)

## Setup Steps

### 1. Initialize EC2 Instance

```bash
# Connect to EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-public-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Reboot to apply user group changes
sudo reboot
```

### 2. Clone Repository

```bash
# After reboot, reconnect
ssh -i your-key.pem ubuntu@your-ec2-public-ip

# Create deployment directory
mkdir -p /home/ubuntu/mlops-parking-detector
cd /home/ubuntu/mlops-parking-detector

# Clone repository
git clone https://github.com/your-username/mlops-project.git .
```

### 3. Configure Environment

```bash
# Create .env file for Docker Compose
cat > .env << EOF
# No additional environment variables needed for basic setup
EOF

# Ensure models directory exists
mkdir -p models/parking/yolov8
mkdir -p models/parking/yolov11
```

### 4. Deploy Application

```bash
# Build and start services
docker-compose build
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f app
```

### 5. Verify Deployment

```bash
# Test backend API
curl http://localhost:3000/health

# Test frontend (should be accessible via browser)
curl http://localhost:5173
```

## GitHub Actions Setup

### Required Secrets

Configure these secrets in your GitHub repository:

1. `EC2_HOST`: Your EC2 public IP address
2. `EC2_USER`: ubuntu (default for Ubuntu AMI)
3. `EC2_SSH_KEY`: Your private SSH key content
4. `EC2_PORT`: 22 (default)
5. `EC2_DEPLOY_PATH`: /home/ubuntu/mlops-parking-detector

### Automated Deployment

The workflow triggers on:
- Push to main branch
- Changes in: config/model_config.yaml, src/**, Dockerfile, requirements*.txt, docker-compose.yml

## Accessing Services

- **Frontend**: http://your-ec2-ip:5173
- **Backend API**: http://your-ec2-ip:3000
- **Prometheus**: http://your-ec2-ip:9090 (if accessible)
- **Grafana**: http://your-ec2-ip:3001 (admin/admin)

## Troubleshooting

### Common Issues

1. **NumPy Compatibility**: Fixed in requirements.txt (numpy==1.26.4)
2. **Port Conflicts**: Ensure ports 3000, 5173 are available
3. **Memory Issues**: Upgrade to t3.large if OOM errors occur
4. **Permission Issues**: Ensure docker group membership

### Logs and Monitoring

```bash
# View application logs
docker-compose logs -f app

# View system resources
docker stats

# Check disk space
df -h
```

## Cost Optimization

- Use t3.medium for development/testing
- Enable EC2 instance scheduling for non-production
- Monitor CloudWatch metrics for scaling decisions
- Consider EFS for persistent storage if needed

## Security Considerations

- Restrict monitoring ports (9090, 3001) to your IP
- Use IAM roles for EC2 instead of access keys
- Enable CloudTrail for API auditing
- Regular security updates via apt
- Consider Application Load Balancer for production
