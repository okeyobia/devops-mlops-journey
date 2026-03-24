# Architecture

## Overview

This project implements a cloud-native Book API platform with a modern DevOps toolchain. The architecture leverages containerization, orchestration, infrastructure-as-code, and automated CI/CD for scalable, reliable, and maintainable deployments.

## Architecture Diagram

```mermaid
graph TD
    User[User/API Client]
    User -->|HTTP Requests| API["Book API (FastAPI/Python)"]
    API -->|Containerized| Docker[Docker]
    Docker -->|Orchestrated| K8s[Kubernetes Cluster]
    K8s -->|Managed by| ArgoCD[ArgoCD (GitOps)]
    K8s -->|Provisioned by| Terraform[Terraform IaC]
    API -->|Stores Artifacts| S3[S3/Artifact Storage]
    Dev[Developer/CI Pipeline]
    Dev -->|Push Code| Git[Git Repository]
    Git -->|Triggers| CI[CI/CD Pipeline]
    CI -->|Builds/Pushes| Docker
    CI -->|Deploys Manifests| GitOps[GitOps Repo]
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
