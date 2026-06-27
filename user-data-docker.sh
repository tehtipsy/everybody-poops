#!/bin/bash
set -e

# ── Config ────────────────────────────────────────────────────────────────────
IMAGE="tehtipsy/everybody-poops:latest"   # CHANGE to your actual image
HOST_PORT=2468
CONTAINER_PORT=8000
CONTAINER_NAME="everybody-poops"
# ─────────────────────────────────────────────────────────────────────────────

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_ID=$ID
else
    echo "Cannot detect OS" && exit 1
fi

install_docker_amazon_linux() {
    yum update -y
    yum install -y docker
    systemctl enable docker
    systemctl start docker
}

install_docker_ubuntu() {
    apt-get update -y
    apt-get install -y ca-certificates curl gnupg lsb-release

    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
        | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg

    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
        https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
        > /etc/apt/sources.list.d/docker.list

    apt-get update -y
    apt-get install -y docker-ce docker-ce-cli containerd.io
    systemctl enable docker
    systemctl start docker
}

case "$OS_ID" in
    amzn)   install_docker_amazon_linux ;;
    ubuntu) install_docker_ubuntu ;;
    *)      echo "Unsupported OS: $OS_ID" && exit 1 ;;
esac

# Pull and run the container
docker pull "$IMAGE"

docker run -d \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    -p "${HOST_PORT}:${CONTAINER_PORT}" \
    "$IMAGE"

echo "everybody-poops is running on port ${HOST_PORT}"
