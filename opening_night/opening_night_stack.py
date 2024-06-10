from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    Stack,
    Duration,
    BundlingOptions,
    aws_s3 as s3,
    RemovalPolicy
)

from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion
from constructs import Construct

import lambdas.uploadFilm
import lambdas.uploadFilm.upload_film

class OpeningNightStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "OpeningNightQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        opening_nights_table= dynamodb.Table(
            self, "Opening-Night-Table",
            table_name="opening-night-table",
            partition_key=dynamodb.Attribute(
                name="name",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1,
        )

        opening_nights_bucket = s3.Bucket(self, "Opening-Night-Bucket",
                            bucket_name="opening-night-bucket",
                            removal_policy=RemovalPolicy.DESTROY,  # Remove films_bucket on stack deletion
                            auto_delete_objects=True,  # Automatically delete objects on stack deletion
                            block_public_access = s3.BlockPublicAccess.BLOCK_ALL
                            )
        
        
        # film = films_api.add_resource("{film_id}")
        # film.add_method("GET")                

        # IAM Role for Lambda Functions
        lambda_role = iam.Role(
            self, "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "dynamodb:DescribeTable",
                    "dynamodb:Query",
                    "dynamodb:Scan",
                    "dynamodb:GetItem",
                    "dynamodb:PutItem",
                    "dynamodb:UpdateItem",
                    "dynamodb:DeleteItem",
                    "s3:PutObject",
                    "s3:PutObjectAcl",
                    "s3:GetObject",
                    "s3:GetObjectAcl",
                    "s3:DeleteObject"
                ],
                resources=[opening_nights_table.table_arn, opening_nights_bucket.bucket_arn + "/*"]
            )
        )

        # Function Definitions
        def create_lambda_function(id, handler, include_dir, method, layers):
            function = _lambda.Function(
                self, id,
                runtime=_lambda.Runtime.PYTHON_3_9,
                layers=layers,
                handler=handler,
                code=_lambda.Code.from_asset(include_dir,
                    bundling=BundlingOptions(
                        image=_lambda.Runtime.PYTHON_3_9.bundling_image,
                        command=[
                            "bash", "-c",
                            "pip install --no-cache -r requirements.txt -t /asset-output && cp -r . /asset-output"
                        ],
                    ),),
                memory_size=128,
                timeout=Duration.seconds(10),
                environment={
                    'TABLE_NAME': opening_nights_table.table_name,
                    'BUCKET_NAME': opening_nights_bucket.bucket_name
                },
                role=lambda_role
            )
            fn_url = function.add_function_url(
                auth_type=_lambda.FunctionUrlAuthType.NONE,
                cors=_lambda.FunctionUrlCorsOptions(
                    allowed_origins=["*"]
                )
            )
            
            return function
        
        
        util_layer = PythonLayerVersion(
            self, 'UtilLambdaLayer',
            entry='libs',
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9]
        )

        upload_film_lambda = create_lambda_function(
            "uploadFilm",
            "upload_film.create",
            "lambdas/uploadFilm",
            "POST",
            [util_layer]
        )

        opening_nights_api = apigateway.RestApi(self, "Opening-Night-Api")

        opening_nights_api.root.add_method("ANY")

        films = opening_nights_api.root.add_resource("films")

        upload_film_integration = apigateway.LambdaIntegration(upload_film_lambda)
        films.add_method("POST", upload_film_integration)


        # create_lambda_function(
        #     "downloadFilm",
        #     "download_film.get_one",
        #     "lambdas/downloadFilm",
        #     "GET",
        #     []
        # )
        
