# DevOps Book API

FastAPI microservice that demonstrates a simple in-memory CRUD API for managing books. The project is set up for local development, container builds, automated tests, and Kubernetes deployment to a Minikube cluster.

## Stack
- FastAPI + Pydantic for the REST API
- Pytest for unit tests
- Docker (multi-stage build using `uv` for dependency management)
- Terraform to spin up a Minikube cluster locally
- Kubernetes manifests in `k8s/` for runtime objects (Namespace, Deployment, Service)

## Project Layout
```
app/           # FastAPI application code
tests/         # Pytest suite
k8s/           # Kubernetes manifests (applied with kubectl)
terraform/     # Infrastructure as code for local Minikube cluster
Dockerfile     # Multi-stage container build
pyproject.toml # Poetry-compatible project metadata (managed by uv)
```

## Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) for dependency management (optional but recommended)
- Docker Desktop (or compatible runtime)
- Minikube + kubectl + Terraform (only if you want to reproduce the local Kubernetes setup)

## Local Development
Install dependencies into a virtual environment and run the API with uvicorn:

```bash
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

`GET http://localhost:8000/` returns the service health payload.

### Running Tests

```bash
uv run pytest
```

### Seed Sample Books
Once the API is running locally (or exposed via Kubernetes), you can pre-populate it with canonical titles using the helper script:

```bash
uv run python scripts/create_books.py --base-url http://localhost:8000
```

Pass `--books-file ./path/to/books.json` to load a custom JSON array of book objects.

## Container Image

```bash
docker build -t localhost:5000/fastapi-app:v1 .
docker run -p 8000:8000 localhost:5000/fastapi-app:v1
```

When targeting Minikube, either build the image inside the cluster environment or load it afterward:

```bash
eval "$(minikube -p minikube-dev docker-env)"
docker build -t localhost:5000/fastapi-app:v1 .
```

## Kubernetes Deployment
Kubernetes resources moved out of Terraform and now live in [k8s/deploy.yaml](k8s/deploy.yaml).

```bash
# Make sure Minikube cluster is running (see Terraform section below)
kubectl apply -f k8s/deploy.yaml
kubectl get all -n book-api

# Expose the LoadBalancer service via Minikube tunnel
minikube -p minikube-dev tunnel
# In another terminal:
minikube -p minikube-dev service fastapi-lb -n book-api
```

To remove the deployment:

```bash
kubectl delete -f k8s/deploy.yaml
```

## Terraform + Minikube
`terraform/main.tf` provisions a single-node Minikube cluster (Docker driver) and wires provider credentials for subsequent `kubectl` interactions.

```bash
cd terraform
terraform init
terraform apply

# Tear down the cluster when finished
terraform destroy
```

Once the cluster exists, switch back to the repository root to build images, apply manifests, and run tests against the cluster as needed.

## API Reference (Quick Glance)

| Method | Path            | Description            |
|--------|-----------------|------------------------|
| GET    | `/`             | Health payload         |
| POST   | `/books/`       | Create a book          |
| GET    | `/books/{id}`   | Retrieve a book        |
| PUT    | `/books/{id}`   | Update existing book   |
| DELETE | `/books/{id}`   | Delete a book          |

All endpoints operate against the in-memory `books_db`, so data resets when the process restarts.
