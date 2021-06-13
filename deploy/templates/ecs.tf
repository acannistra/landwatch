resource "aws_ecs_cluster" "app" {
  name = "${var.app}-${var.environment}"
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  capacity_providers = ["FARGATE", "FARGATE_SPOT"]
  tags = var.tags
}
