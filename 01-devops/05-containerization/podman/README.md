# 🦭 Podman — Daemonless Container Engine

> **Podman is a drop-in Docker replacement that runs containers without a daemon and as rootless by default.**

## Docker vs Podman

| Feature | Docker | Podman |
|---------|--------|--------|
| Daemon | Yes (dockerd) | No (daemonless) |
| Root required | Yes (default) | No (rootless default) |
| CLI compatibility | Native | `alias docker=podman` |
| Compose | docker-compose | podman-compose |
| Pods | No native concept | Yes (like K8s pods) |
| Systemd integration | Limited | Native (generate systemd units) |

## Quick Start

```bash
# Install (Fedora/RHEL)
sudo dnf install podman

# Use exactly like Docker
podman pull nginx:alpine
podman run -d -p 8080:80 nginx:alpine
podman ps
podman stop <container-id>

# Rootless — no sudo needed!
podman run --rm -it alpine sh

# Generate Kubernetes YAML from running container
podman generate kube my-container > pod.yaml

# Generate systemd service
podman generate systemd --name my-container > my-container.service
```

## When to Use Podman

- **Security-sensitive environments** (rootless = smaller attack surface)
- **Kubernetes-native workflows** (pod concept, `podman play kube`)
- **CI/CD pipelines** (no daemon = simpler in containers)
- **RHEL/Fedora ecosystems** (native support)

## Further Reading

- [Podman Docs](https://docs.podman.io/)
- [Podman vs Docker](https://www.redhat.com/en/topics/containers/what-is-podman)
