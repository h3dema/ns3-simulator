# ------------------------------------------------------------
# Variables
# ------------------------------------------------------------
SERVICE      := ns3
IMAGE        := ns3-nbiot
COMPOSE      := docker compose
CONTAINER_ID := $(shell docker ps -aq -f name=$(IMAGE))
IMAGE_ID     := $(shell docker images -q $(IMAGE))

# ------------------------------------------------------------
# Targets
# ------------------------------------------------------------

.PHONY: help build run stop clean

help:
	@echo ""
	@echo "Available targets:"
	@echo "  make build   - Build the Docker image"
	@echo "  make run     - Run the container (build if needed)"
	@echo "  make stop    - Stop the running container"
	@echo "  make clean   - Stop container and remove image"
	@echo ""

# ------------------------------------------------------------

build:
	@echo "🔧 Building image: $(IMAGE)"
	$(COMPOSE) build $(SERVICE)

# ------------------------------------------------------------

run:
	@if [ -z "$(IMAGE_ID)" ]; then \
		echo "📦 Image not found. Building first..."; \
		$(COMPOSE) build $(SERVICE); \
	fi
	@echo "🚀 Running container: $(IMAGE)"
	$(COMPOSE) run --rm $(SERVICE)

# ------------------------------------------------------------

stop:
	@if [ -n "$(CONTAINER_ID)" ]; then \
		echo "🛑 Stopping container: $(IMAGE)"; \
		docker stop $(CONTAINER_ID); \
	else \
		echo "ℹ️ No running container to stop."; \
	fi

# ------------------------------------------------------------

clean: stop
	@if [ -n "$(IMAGE_ID)" ]; then \
		echo "🧹 Removing image: $(IMAGE)"; \
		docker rmi -f $(IMAGE_ID); \
	else \
		echo "ℹ️ No image to remove."; \
	fi
	@if [ -n "$(CONTAINER_ID)" ]; then \
		echo "🧹 Removing stopped container: $(IMAGE)"; \
		docker rm -f $(CONTAINER_ID); \
	fi
