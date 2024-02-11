from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw
)
from .hitcounter_construct import HitCounterConstruct
from .vpc_construct import VpcConstruct


class CdkWorkshopStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_lambda = _lambda.Function(
            self, "HelloHandler",
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='hello.handler'
        )

        hello_with_counter = HitCounterConstruct(
            self, 'HelloHitCounter',
            downstream=my_lambda,
        )

        my_vpc = VpcConstruct(self, 'CustomVPCByCDK')

        api = apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=hello_with_counter.handler
        )

        # Add a resource for the '/vpc' path
        vpc_resource = api.root.add_resource('vpc')
        # Add a method to the '/vpc' resource that integrates with the VPC Lambda
        vpc_resource.add_method('ANY', apigw.LambdaIntegration(my_vpc.handler))

        # Add a method to the '/vpc/*' resource that integrates with the VPC Lambda
        vpc_resource.add_resource('{proxy+}').add_method('ANY', apigw.LambdaIntegration(my_vpc.handler))