resource "kubernetes_deployment" "fastapi_app" {
  metadata {
    name = "fastapi-service"
    namespace = "book-api"
    labels = {
      app = "fastapi"
    }
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "fastapi"
      }
    }

    template {
      metadata {
        labels = {
          app = "fastapi"
        }
      }

      spec {
        container {
          image = "localhost:5000/fastapi-app:v1" # Point to minikube's registry
          name  = "fastapi"

          port {
            container_port = 8000
          }

          resources {
            limits = {
              cpu    = "0.5"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "256Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "fastapi_svc" {
  metadata {
    name = "fastapi-lb"
    namespace = "book-api"
  }
  spec {
    selector = {
      app = kubernetes_deployment.fastapi_app.metadata[0].name
    }
    port {
      port        = 80
      target_port = 8000
    }
    type = "LoadBalancer"
  }
}