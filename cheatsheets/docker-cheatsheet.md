# 🐳 Docker Cheatsheet

> Quick reference for Docker commands you'll use daily.

---

## 📦 Images

```bash
docker images                            # List local images
docker pull nginx:alpine                 # Pull image
docker build -t myapp:v1 .              # Build image
docker build -t myapp:v1 -f Dockerfile.prod .  # Custom Dockerfile
docker tag myapp:v1 registry/myapp:v1   # Tag for registry
docker push registry/myapp:v1           # Push to registry
docker rmi <image>                      # Remove image
docker image prune -a                   # Remove unused images
docker history <image>                  # Show image layers
docker inspect <image>                  # Detailed image info
```

## 🐳 Containers

```bash
docker run -d -p 8080:3000 --name myapp myapp:v1  # Run detached
docker run -it ubuntu:22.04 bash        # Interactive shell
docker run --rm -it alpine sh           # Temporary container
docker run -v $(pwd):/app -w /app node npm test  # Mount volume
docker run --env-file .env myapp:v1     # Load env file
docker ps                               # Running containers
docker ps -a                            # All containers
docker stop <container>                 # Graceful stop
docker kill <container>                 # Force stop
docker rm <container>                   # Remove container
docker logs <container> -f              # Follow logs
docker exec -it <container> sh          # Shell into container
docker stats                            # Resource usage (live)
docker inspect <container>              # Container details
docker cp <container>:/path ./local     # Copy from container
```

## 🏗️ Docker Compose

```bash
docker compose up -d                     # Start all services
docker compose down                      # Stop and remove
docker compose down -v                   # Also remove volumes
docker compose logs -f <service>         # Follow service logs
docker compose ps                        # Service status
docker compose build                     # Rebuild images
docker compose up -d --scale api=3       # Scale a service
docker compose exec api sh              # Shell into service
docker compose pull                     # Pull latest images
docker compose config                   # Validate compose file
```

## 💾 Volumes & Networks

```bash
docker volume ls                         # List volumes
docker volume create mydata              # Create volume
docker volume inspect mydata             # Volume details
docker volume rm mydata                  # Remove volume
docker network ls                        # List networks
docker network create mynet              # Create network
docker network inspect mynet             # Network details
```

## 🧹 Cleanup

```bash
docker system prune                      # Remove unused data
docker system prune -af --volumes        # Nuclear cleanup
docker container prune                   # Remove stopped containers
docker image prune -a                    # Remove unused images
docker volume prune                      # Remove unused volumes
docker system df                         # Disk usage summary
```

## 🔍 Debugging

```bash
docker logs <container> --since 1h       # Logs from last hour
docker inspect --format='{{.State.ExitCode}}' <container>  # Exit code
docker diff <container>                  # Changed files in container
docker top <container>                   # Running processes
docker events                           # Real-time Docker events
```

---

> 💡 **Tip:** Use [Dive](https://github.com/wagoodman/dive) to analyze image layers and reduce size.
