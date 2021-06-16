import os
from prefect.storage import S3
from prefect.run_configs import ECSRun

ECS_CLUSTER_NAME = os.environ.get("ECS_CLUSTER_NAME", 'landwatch-dev')
INFRA_BUCKET_NAME = os.environ.get("INFRA_BUCKET_NAME", 'us.landwatch.infra')

S3_STORAGE = S3(
    bucket = INFRA_BUCKET_NAME
)

ECS_RUNNER = ECSRun(
    run_task_kwargs={
        "cluster": ECS_CLUSTER_NAME
    }, 
    execution_role_arn="arn:aws:iam::802903626273:role/ECSTaskExecutionRole", 
    image='802903626273.dkr.ecr.us-west-2.amazonaws.com/landwatch'
)