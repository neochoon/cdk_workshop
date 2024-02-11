from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_lambda as _lambda,
)

class VpcConstruct(Construct):
    @property
    def handler(self):
        return self._handler

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a new VPC
        self.vpc = ec2.Vpc(
            self, "CustomVPCByCDK",
            max_azs=3,  # Default is all AZs in the region
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                )
            ]
        )

        self._handler = _lambda.Function(
            self, "HelloFromVPCHandler",
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='hello_from_vpc.handler',
            vpc=self.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
        )