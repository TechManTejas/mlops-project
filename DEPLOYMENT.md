# Deployment Guide

## EC2 Environment Setup

### Required GitHub Secrets

Add these secrets to your GitHub repository settings:

1. **EC2_HOST** - Your EC2 instance public IP or DNS
2. **EC2_USER** - SSH username (usually `ec2-user` or `ubuntu`)
3. **EC2_SSH_KEY** - Private SSH key content (not file path)
4. **EC2_PORT** - SSH port (default: 22, optional)
5. **EC2_DEPLOY_PATH** - Path to project on EC2 (e.g., `/home/ubuntu/mlops-project`)

### EC2 Instance Prerequisites

1. **Install Docker and Docker Compose**
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker $USER
```

2. **Install Git**
```bash
sudo apt install git -y
```

3. **Install DVC**
```bash
pip install dvc[s3]
```

4. **Clone Repository**
```bash
git clone <your-repo-url> $EC2_DEPLOY_PATH
cd $EC2_DEPLOY_PATH
```

5. **Configure DVC Remote** (if using S3)
```bash
dvc remote add -d myremote s3://your-bucket-name
dvc remote modify myremote access_key_id $AWS_ACCESS_KEY_ID
dvc remote modify myremote secret_access_key $AWS_SECRET_ACCESS_KEY
```

### Deployment Process

The GitHub Actions workflow will automatically:
1. SSH into your EC2 instance
2. Pull latest code changes
3. Run `dvc pull` to get models
4. Restart Docker containers

### Manual Deployment Commands

```bash
cd $EC2_DEPLOY_PATH
git fetch --all
git reset --hard origin/main
dvc pull
docker compose down
docker compose up -d --build
```

### Service URLs

- **Backend API**: http://localhost:3000 (internal only)
- **Frontend**: http://localhost:5173 (publicly accessible)
- **Health Check**: http://localhost:3000/health

### Model Version Management

To switch models:
1. Edit `config/serving.yaml`
2. Change `active_model_version: v1` to `active_model_version: v2`
3. Push to main branch
4. GitHub Actions will auto-deploy the change

### Troubleshooting

1. **Check container status**: `docker ps`
2. **View logs**: `docker logs mlops-parking-detector`
3. **Restart services**: `docker compose restart`
4. **Check model files**: `ls -la models/parking/v1/`
