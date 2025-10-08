# 🐳 Docker Deployment Guide

This guide explains how to run the AI Email Generator using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed (20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) installed (1.29+)
- OpenAI API Key

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/ai-email-generator.git
cd ai-email-generator
```

### 2. Configure Environment

Create a `.env` file with your API key:

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

Or set it directly in docker-compose:

```bash
export OPENAI_API_KEY=your_api_key_here
```

### 3. Build and Run

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### 4. Access the Application

Open your browser and navigate to:
```
http://localhost:8501
```

## Docker Commands

### Basic Operations

```bash
# Build the image
docker-compose build

# Start containers in background
docker-compose up -d

# Start containers with build
docker-compose up -d --build

# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Stop containers
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers with volumes
docker-compose down -v
```

### Maintenance

```bash
# Restart the service
docker-compose restart

# Execute commands inside container
docker-compose exec ai-email-generator bash

# View resource usage
docker stats ai-email-generator

# Clean up unused images
docker image prune -a
```

## Configuration

### Environment Variables

Configure the application by setting environment variables in `.env` or `docker-compose.yml`:

```yaml
environment:
  - OPENAI_API_KEY=your_key_here
  - OPENAI_MODEL=gpt-3.5-turbo
  - OPENAI_MAX_TOKENS=350
  - OPENAI_TEMPERATURE=0.7
  - LOG_LEVEL=INFO
```

### Persistent Data

The following directories are mounted as volumes for data persistence:

- `./data` - Database and data files
- `./logs` - Application logs
- `./exports` - Exported emails

### Resource Limits

Adjust resource limits in `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
    reservations:
      cpus: '1'
      memory: 1G
```

## Production Deployment

### Using Docker Only (No Compose)

```bash
# Build image
docker build -t ai-email-generator .

# Run container
docker run -d \
  --name ai-email-generator \
  -p 8501:8501 \
  -e OPENAI_API_KEY=your_key_here \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  ai-email-generator
```

### With Nginx Reverse Proxy

Uncomment the nginx service in `docker-compose.yml` and create `nginx.conf`:

```nginx
upstream streamlit {
    server ai-email-generator:8501;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL/HTTPS Setup

1. Obtain SSL certificate (e.g., Let's Encrypt)
2. Mount certificates in nginx service
3. Update nginx.conf for HTTPS

## Health Checks

The container includes a health check:

```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' ai-email-generator

# Manual health check
curl http://localhost:8501/_stcore/health
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs ai-email-generator

# Check if port is in use
lsof -i :8501

# Verify environment variables
docker-compose config
```

### Permission Issues

```bash
# Fix permissions for mounted volumes
sudo chown -R $USER:$USER data/ logs/ exports/
```

### API Connection Issues

```bash
# Verify API key is set
docker-compose exec ai-email-generator env | grep OPENAI

# Test API connectivity
docker-compose exec ai-email-generator python -c "from openai import OpenAI; print(OpenAI().models.list())"
```

### Reset Everything

```bash
# Stop and remove containers, networks, and volumes
docker-compose down -v

# Remove images
docker rmi ai-email-generator

# Rebuild from scratch
docker-compose up -d --build --force-recreate
```

## Performance Tips

1. **Use BuildKit** for faster builds:
   ```bash
   DOCKER_BUILDKIT=1 docker-compose build
   ```

2. **Multi-stage builds** are already configured to minimize image size

3. **Volume mounts** ensure data persistence across container restarts

4. **Resource limits** prevent container from consuming excessive resources

## Security Best Practices

1. **Never commit `.env` file** with real API keys
2. **Use secrets** for production:
   ```yaml
   secrets:
     openai_key:
       external: true
   ```

3. **Run as non-root user** (add to Dockerfile):
   ```dockerfile
   RUN useradd -m -u 1000 appuser
   USER appuser
   ```

4. **Keep base image updated**:
   ```bash
   docker pull python:3.11-slim
   docker-compose build --no-cache
   ```

## Cloud Deployment

### AWS ECS

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
docker tag ai-email-generator:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/ai-email-generator:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/ai-email-generator:latest
```

### Google Cloud Run

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/ai-email-generator
gcloud run deploy --image gcr.io/PROJECT-ID/ai-email-generator --platform managed
```

### Azure Container Instances

```bash
# Build and push to ACR
az acr build --registry myregistry --image ai-email-generator .
az container create --resource-group myResourceGroup --name ai-email-generator --image myregistry.azurecr.io/ai-email-generator
```

## Support

For Docker-related issues:
- Check [Docker Documentation](https://docs.docker.com/)
- Review container logs: `docker-compose logs`
- Verify configuration: `docker-compose config`

For application issues, see main README.md

