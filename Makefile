# Local helpers for the Fake Adjust API.
#
# The stage-2 consumer lives in a separate repository:
#   https://github.com/Gasta88/fake_adjust_serverless_service

IMAGE_NAME := fake_adjust
IMAGE_TAG := latest
CONTAINER_NAME := fake_adjust
DOCKERFILE := Dockerfile
PYTHON ?= python3

.PHONY: help install-dev build run clean all test lint

help:
	@echo "make install-dev   Install runtime and development dependencies"
	@echo "make build         Build the Docker image"
	@echo "make run           Run the API container on port 8000"
	@echo "make all           build + run"
	@echo "make clean         Remove the container and image"
	@echo "make test          Run the test suite"
	@echo "make lint          Run ruff"

install-dev:
	$(PYTHON) -m pip install -r requirements-dev.txt

build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) -f $(DOCKERFILE) .

run:
	@docker rm -f $(CONTAINER_NAME) >/dev/null 2>&1 || true
	docker run -d --name $(CONTAINER_NAME) -p 8000:8000 $(IMAGE_NAME):$(IMAGE_TAG)
	@echo "API available at http://127.0.0.1:8000"

clean:
	@docker rm -f $(CONTAINER_NAME) || true
	@docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true

all: build run

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check .
