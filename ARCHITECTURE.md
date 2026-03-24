# Architecture

## Overview

This project implements a cloud-native Book API platform with a modern DevOps toolchain. The architecture leverages containerization, orchestration, infrastructure-as-code, and automated CI/CD for scalable, reliable, and maintainable deployments.

## Architecture Diagram

```mermaid
graph TD
    User["User/API Client"]
    API["Book API (FastAPI/Python)"]
    Docker["Docker"]
    K8s["Kubernetes Cluster"]
    ArgoCD["ArgoCD (GitOps)"]
    Terraform["Terraform IaC"]
    S3["S3/Artifact Storage"]
    Dev["Developer/CI Pipeline"]
    Git["Git Repository"]
    CI["CI/CD Pipeline"]
    GitOps["GitOps Repo"]

    User -->|HTTP Requests| API
    API -->|Containerized| Docker
    Docker -->|Orchestrated| K8s
    K8s -->|Managed by| ArgoCD
    K8s -->|Provisioned by| Terraform
    API -->|Stores Artifacts| S3
    Dev -->|Push Code| Git
    Git -->|Triggers| CI
    CI -->|Builds/Pushes| Docker
    CI -->|Deploys Manifests| GitOps
    GitOps -->|Syncs| ArgoCD
    ArgoCD -->|Deploys| K8s
```

## Highlights

- Microservices-based Book API built with Python
- Containerized using Docker for consistent deployments
- Kubernetes orchestrates scalable, resilient workloads
- Infrastructure managed as code with Terraform
- Automated CI/CD pipelines for build, test, and deployment
- ArgoCD enables GitOps-driven, declarative deployments
- Secure configuration and environment management
- Zero-downtime rolling updates and rollback support
- Modular design for easy extensibility and maintenance
