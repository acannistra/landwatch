resource "aws_ecs_cluster" "app" {
  name = "${var.app}-${var.environment}"
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  capacity_providers = ["FARGATE", "FARGATE_SPOT"]
  tags = var.tags
}

resource "aws_iam_role" "taskexecrole" {
  name = "ECSTaskExecutionRole"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy" 
  ]
}