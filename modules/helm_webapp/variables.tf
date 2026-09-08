variable "helm_release_name" {
  description = "Name of the Helm release"
  type        = string
}

variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
}

variable "image_repository" {
  description = "Docker image repository"
  type        = string
}

variable "image_tag" {
  description = "Docker image tag"
  type        = string
  default     = "latest"
}

variable "hello_world_message" {
  description = "Message for the hello world endpoint"
  type        = string
  default     = "Hello, World!"
}