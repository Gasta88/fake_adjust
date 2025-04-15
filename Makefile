# Define variables
IMAGE_NAME := fake_adjust
IMAGE_TAG := latest
DOCKERFILE := Dockerfile
SOURCE_DIR := .

# Build the Docker image
build: $(SOURCE_DIR)/* $(DOCKERFILE)
	@echo "Building Docker image..."
	@if ! docker build -t $(IMAGE_NAME):$(IMAGE_TAG) -f $(DOCKERFILE) $(SOURCE_DIR); then \
        echo "Docker image build failed."; \
        exit 1; \
	fi

# Run the Docker container
run:
	@echo "Running Docker container..."
	@if ! docker run -d -p 8000:8000 $(IMAGE_NAME):$(IMAGE_TAG); then \
        echo "Docker container failed to start."; \
        exit 1; \
	fi
	@echo "Docker container is running. API is available at http://127.0.0.1:8000"

# Clean up Docker resources
clean:
	@echo "Cleaning up Docker resources..."
	@docker rm -f $(shell docker ps -aq -f ancestor=$(IMAGE_NAME):$(IMAGE_TAG)) || true
	@docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true

# Default target
all: build run

.PHONY: build run clean all