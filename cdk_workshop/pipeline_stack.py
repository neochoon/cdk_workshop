from typing import Any, Dict, Mapping
from constructs import Construct
from aws_cdk import (
    Environment,
    IStackSynthesizer,
    PermissionsBoundary,
    Stack,
    aws_codecommit as codecommit,
)

class WorkshopPipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        repo = codecommit.Repository(self, "WorkshopRepo",
            repository_name="cdk-workshop-repo"
        )