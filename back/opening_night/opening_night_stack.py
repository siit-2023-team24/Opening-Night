from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    Stack,
    Duration,
    BundlingOptions,
    aws_s3 as s3,
    RemovalPolicy,
    aws_cognito as cognito,
    aws_ssm as ssm
)

from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion
from constructs import Construct

class OpeningNightStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        user_roles = ['admin', 'viewer']

        user_pool = cognito.UserPool(self, "Opening-Night-User-Pool",
            user_pool_name="opening-night-user-pool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(
                username=True
            ),
            auto_verify=cognito.AutoVerifiedAttrs(
                email=False
            ),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=True
            ),
            account_recovery=cognito.AccountRecovery.NONE,
        )

        user_pool_client = user_pool.add_client("OpeningNightUserPoolClient",
            user_pool_client_name="opening-night-user-pool-client",
            auth_flows=cognito.AuthFlow(
                user_password=True
            ),
            generate_secret=False
        )

        ssm.StringParameter(self, "UserPoolId",
            parameter_name="pool_id",
            string_value=user_pool.user_pool_id
        )

        ssm.StringParameter(self, "UserPoolClientId",
            parameter_name="client_id",
            string_value=user_pool_client.user_pool_client_id
        )

        opening_nights_table= dynamodb.Table(
            self, "Opening-Night-Table",
            table_name="opening-night-table",
            partition_key=dynamodb.Attribute(
                name="fileName",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1,
        )

        opening_nights_bucket = s3.Bucket(self, "Opening-Night-Bucket",
            bucket_name="opening-night-bucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access = s3.BlockPublicAccess.BLOCK_ALL
            )           
        
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
                    "s3:DeleteObject",
                    "ssm:GetParameter", # register, login
                    "cognito-idp:AdminConfirmSignUp", # register
                    "cognito-idp:ListUsers" # register
                ],
                resources=[opening_nights_table.table_arn,
                           opening_nights_bucket.bucket_arn + "/*",
                           "arn:aws:ssm:eu-central-1:339713060982:parameter/client_id", # register, login
                           "arn:aws:ssm:eu-central-1:339713060982:parameter/pool_id", # login
                           f"arn:aws:cognito-idp:eu-central-1:339713060982:userpool/{user_pool.user_pool_id}"] # register
            )
        )
        #TODO razdvojiti prava

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

        download_film_lambda = create_lambda_function(
            "downloadFilm",
            "download_film.get_one",
            "lambdas/downloadFilm",
            "GET",
            []
        )

        login_lambda = create_lambda_function(
            "login",
            "login.login",
            "lambdas/login",
            "POST",
            []
        )

        register_lambda = create_lambda_function(
            "register",
            "register.register",
            "lambdas/register",
            "POST",
            []
        )

        opening_nights_api = apigateway.RestApi(self, "Opening-Night-Api")
        opening_nights_api.root.add_method("ANY")

        films = opening_nights_api.root.add_resource("films")
        upload_film_integration = apigateway.LambdaIntegration(upload_film_lambda)
        films.add_method("POST", upload_film_integration)

        film = opening_nights_api.root.add_resource("{name}")
        download_film_integration = apigateway.LambdaIntegration(download_film_lambda)
        film.add_method("GET", download_film_integration)

        login = opening_nights_api.root.add_resource("login")
        login_integration = apigateway.LambdaIntegration(login_lambda)
        login.add_method("POST", login_integration)

        register = opening_nights_api.root.add_resource("register")
        register_integration = apigateway.LambdaIntegration(register_lambda)
        register.add_method("POST", register_integration)