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
    aws_sqs as sqs,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_lambda_event_sources as eventsources,
    aws_cognito as cognito,
    aws_ssm as ssm,
    aws_sqs as sqs,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
)

from aws_cdk.aws_lambda_python_alpha import PythonLayerVersion
from constructs import Construct

class OpeningNightStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        user_roles = ['admin', 'viewer']

        user_pool = cognito.UserPool(self, "Opening-Night-Pool",
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
            custom_attributes={
                "is_viewer": cognito.BooleanAttribute()
            }
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
            self, "Films-Table",
            table_name="films-table",
            partition_key=dynamodb.Attribute(
                name="filmId",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1,
        )

        subs_table= dynamodb.Table(
            self, "Subscriptions-Table",
            table_name="subscriptions-table",
            partition_key=dynamodb.Attribute(
                name="username",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1,
        )

        ratings_table= dynamodb.Table(
            self, "Ratings-Table",
            table_name="ratings-table",
            partition_key=dynamodb.Attribute(name="filmId", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="username", type=dynamodb.AttributeType.STRING),
            read_capacity=1,
            write_capacity=1,
        )

        ratings_table.add_global_secondary_index(
            index_name='username-index',
            partition_key=dynamodb.Attribute(name='username', type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name='filmId', type=dynamodb.AttributeType.STRING),
            projection_type=dynamodb.ProjectionType.ALL
        )

        downloads_log_table = dynamodb.Table(
            self, "Downloads-Log-Table",
            table_name="downloads-log-table",
            partition_key=dynamodb.Attribute(name="username", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="timestamp", type=dynamodb.AttributeType.STRING),
            read_capacity=1,
            write_capacity=1
        )

        feed_table = dynamodb.Table(
            self, "Feed-Table",
            table_name="feed-table",
            partition_key=dynamodb.Attribute(name="username", type=dynamodb.AttributeType.STRING),
            read_capacity=1,
            write_capacity=1
        )

        opening_nights_bucket = s3.Bucket(self, "Opening-Night-Bucket",
            bucket_name="opening-night-bucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access = s3.BlockPublicAccess.BLOCK_ALL
        )

        feed_queue = sqs.Queue(
            self, "FeedQueue",
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
                           subs_table.table_arn,
                           ratings_table.table_arn,
                           f"{ratings_table.table_arn}/index/username-index",
                           downloads_log_table.table_arn,
                           feed_table.table_arn,
                           opening_nights_bucket.bucket_arn + "/*",
                           "arn:aws:ssm:eu-central-1:339713060982:parameter/client_id", # register, login
                           "arn:aws:ssm:eu-central-1:339713060982:parameter/pool_id", # login
                           f"arn:aws:cognito-idp:eu-central-1:339713060982:userpool/{user_pool.user_pool_id}"] # register
            )
        )

        
        #TODO razdvojiti prava



        def create_lambda_function(id, handler, include_dir, method, layers, role=lambda_role, env_var=''):
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
                        ]
                    ),),
                memory_size=128,
                timeout=Duration.seconds(30),
                environment={
                    'TABLE_NAME': opening_nights_table.table_name,
                    'SUBS_TABLE_NAME': subs_table.table_name,
                    'RATINGS_TABLE_NAME': ratings_table.table_name,
                    'DOWNLOADS_TABLE_NAME': downloads_log_table.table_name,
                    'FEED_TABLE_NAME': feed_table.table_name,
                    'BUCKET_NAME': opening_nights_bucket.bucket_name,
                    'CUSTOM_VAR': env_var
                },
                role=role
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

        ffmpeg_layer = _lambda.LayerVersion(
            self, 'FFmpegLayer',
            code=_lambda.AssetCode('lambda_layers/ffmpeg_layer'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
            description='FFmpeg layer',
        )
        
        authorize_viewer_lambda = create_lambda_function(
            "authorizeViewer",
            "authorize_viewer.authorize",
            "lambdas/authorization",
            "GET",
            []
        )

        authorize_admin_lambda = create_lambda_function(
            "authorizeAdmin",
            "authorize_admin.authorize",
            "lambdas/authorization",
            "GET",
            []
        )

        # authorizer = apigateway.CognitoUserPoolsAuthorizer(self, "CognitoAuthorizer",
        #     cognito_user_pools=[user_pool]
        # )

        # viewer_authorizer = apigateway.RequestAuthorizer(self, "ViewerAuthorizer",
        #     handler = authorize_viewer_lambda,
        #     identity_sources=[apigateway.IdentitySource.header("Authorization")],
        #     results_cache_ttl=Duration.seconds(0)
        # )

        # admin_authorizer = apigateway.RequestAuthorizer(self, "AdminAuthorizer",
        #     handler = authorize_admin_lambda,
        #     identity_sources=[apigateway.IdentitySource.header("Authorization")],
        #     results_cache_ttl=Duration.seconds(0)
        # )
        
        # trans_layer = PythonLayerVersion(
        #     self, 'TransLambdaLayer',
        #     entry='lambda_layers/ffmpeg_layer',
        #     compatible_runtimes=[_lambda.Runtime.PYTHON_3_9]
        # )

        download_film_lambda = create_lambda_function(
            "downloadFilm",
            "download_film.get_one",
            "lambdas/downloadFilm",
            "GET",
            []
        )

        update_subscriptions_lambda = create_lambda_function(
            "updateSubscriptions",
            "update_subscriptions.update_subs",
            "lambdas/updateSubscriptions",
            "POST",
            [],
            env_var=feed_queue.queue_url
          )  

        get_subscriptions_lambda = create_lambda_function(
            "getSubscriptions",
            "get_subscriptions.get_subs",
            "lambdas/getSubscriptions",
            "GET",
            []
        )

        get_actors_and_directors_lambda = create_lambda_function(
            "getActorsAndDirectors",
            "get_actors_and_directors.get_actors_and_directors",
            "lambdas/getActorsAndDirectors",
            "GET",
            []
        )

        get_film_by_id_lambda = create_lambda_function(
            "getFilmById",
            "get_film_by_id.get_film",
            "lambdas/getFilmById",
            "GET",
            []
        )

        get_film_by_id_update_lambda = create_lambda_function(
            "getFilmByIdUpdate",
            "get_film_by_id_update.get_film",
            "lambdas/getFilmByIdUpdate",
            "GET",
            []
        )

        update_film_lambda = create_lambda_function(
            "updateFilm",
            "update_film.update",
            "lambdas/updateFilm",
            "PUT",
            []
        )

        get_all_films_lambda = create_lambda_function(
            "getAllFilms",
            "get_all_films.get",
            "lambdas/getAllFilms",
            "GET",
            []
        )

        get_series_list_lambda = create_lambda_function(
            "getSeriesList",
            "get_series_list.get",
            "lambdas/getSeriesList",
            "GET",
            []
        )

        get_episodes_by_series_lambda = create_lambda_function(
            "getEpisodesBySeries",
            "get_episodes_by_series.get",
            "lambdas/getEpisodesBySeries",
            "GET",
            []
        )

        get_ratings_for_film_lambda = create_lambda_function(
            "getRatingForFilm",
            "get_ratings_for_film.get_ratings_for_film",
            "lambdas/getRatingsForFilm",
            "GET",
            []
        )

        rate_film_lambda = create_lambda_function(
            "rateFilm",
            "rate_film.rate",
            "lambdas/rateFilm",
            "POST",
            [],
            env_var=feed_queue.queue_url
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

        # Upload film step

        upload_film_original_lambda = create_lambda_function(
            "uploadOriginal",
            "upload_film_original.create",
            "lambdas/uploadOriginal",
            "",
            [ffmpeg_layer]
        )

        upload_film_360p_lambda = create_lambda_function(
            "upload360p",
            "upload_film_360p.create",
            "lambdas/upload360p",
            "",
            [ffmpeg_layer]
        )

        upload_film_144p_lambda = create_lambda_function(
            "upload144p",
            "upload_film_144p.create",
            "lambdas/upload144p",
            "",
            [ffmpeg_layer]
        )

        write_info_lambda = create_lambda_function(
            "writeInfo",
            "write_info.create",
            "lambdas/writeInfo",
            "",
            []
        )

        write_info_task = tasks.LambdaInvoke(
            self, "WriteInfoTask",
            lambda_function=write_info_lambda,
            output_path='$'
        )

        upload_film_original_task = tasks.LambdaInvoke(
            self, "UploadFilmOriginalTask",
            lambda_function=upload_film_original_lambda,
            input_path='$.Payload'
        )

        upload_film_360p_task = tasks.LambdaInvoke(
            self, "UploadFilm360pTask",
            lambda_function=upload_film_360p_lambda,
            input_path='$.Payload'
        )

        upload_film_144p_task = tasks.LambdaInvoke(
            self, "UploadFilm144pTask",
            lambda_function=upload_film_144p_lambda,
            input_path='$.Payload'
        )

        upload_parallel_tasks = sfn.Parallel(self, "UploadParallelTasks", input_path='$')
        upload_parallel_tasks.branch(sfn.Chain.start(upload_film_original_task))
        upload_parallel_tasks.branch(sfn.Chain.start(upload_film_360p_task))
        upload_parallel_tasks.branch(sfn.Chain.start(upload_film_144p_task))

        write_info_task.next(upload_parallel_tasks)

        upload_definition = write_info_task

        upload_step_function = sfn.StateMachine(
            self, "UploadStateMachine",
            definition_body=sfn.DefinitionBody.from_chainable(upload_definition),
            comment='Upload film'
        )

        upload_lambda_role = iam.Role(
            self, "UploadLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        upload_lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )
        upload_lambda_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "states:StartExecution",
                    "s3:PutObject",
                    "s3:PutObjectAcl",
                    "s3:GetObject",
                    "s3:GetObjectAcl",
                    "s3:DeleteObject"
                ],
                resources=[
                           upload_step_function.state_machine_arn,
                           opening_nights_bucket.bucket_arn + "/*"
                        ]
            )
        )

        upload_film_lambda = create_lambda_function(
            "uploadFilm",
            "upload_film.upload",
            "lambdas/uploadFilm",
            "POST",
            [],
            upload_lambda_role,
            upload_step_function.state_machine_arn
        )

        get_feed_lambda = create_lambda_function(
            "getFeed",
            "get_feed.get_feed",
            "lambdas/getFeed",
            "GET",
            []
        )

        #Feed step

        calc_downloads_score_lambda = create_lambda_function(
            "calcDownloadsScore",
            "calc_downloads_score.calc_downloads_score",
            "lambdas/calcDownloadsScore",
            "",
            []
        )

        calc_ratings_score_lambda = create_lambda_function(
            "calcRatingsScore",
            "calc_ratings_score.calc_ratings_score",
            "lambdas/calcRatingsScore",
            "",
            []
        )

        calc_subs_score_lambda = create_lambda_function(
            "calcSubscriptionsScore",
            "calc_subscriptions_score.calc_subs_score",
            "lambdas/calcSubscriptionsScore",
            "",
            []
        )

        determine_feed_lambda = create_lambda_function(
            "determineFeed",
            "determine_feed.determine_feed",
            "lambdas/determineFeed",
            "",
            []
        )

        calc_downloads_score_task = tasks.LambdaInvoke(
            self, "CalcDownloadsScoreTask",
            lambda_function=calc_downloads_score_lambda,
            output_path="$.Payload.Download"
        )

        calc_ratings_score_task = tasks.LambdaInvoke(
            self, "CalcRatingsScoreTask",
            lambda_function=calc_ratings_score_lambda,
            output_path="$.Payload.Rating"
        )

        calc_subs_score_task = tasks.LambdaInvoke(
            self, "CalcSubscriptionsScoreTask",
            lambda_function=calc_subs_score_lambda,
            output_path="$.Payload.Subs"
        )

        feed_parallel_tasks = sfn.Parallel(self, "FeedParallelTasks",
            result_selector={
                "Download.$": "$[0]",
                "Rating.$": "$[1]",
                "Subs.$": "$[2]"
            },
            result_path="$.Payload")
        feed_parallel_tasks.branch(sfn.Chain.start(calc_downloads_score_task))
        feed_parallel_tasks.branch(sfn.Chain.start(calc_ratings_score_task))
        feed_parallel_tasks.branch(sfn.Chain.start(calc_subs_score_task))

        determine_feed_task = tasks.LambdaInvoke(
            self, "DetermineFeedTask",
            lambda_function=determine_feed_lambda,
            input_path="$.Payload"
        )

        feed_parallel_tasks.next(determine_feed_task)

        feed_definition = feed_parallel_tasks

        feed_step_function = sfn.StateMachine(
            self, "FeedStateMashine",
            definition_body=sfn.DefinitionBody.from_chainable(feed_definition),
            comment='Determine and persist feed for user'
        )

        feed_lambda_role = iam.Role(
            self, "FeedLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        feed_lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )
        feed_lambda_role.add_to_policy(
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
                    "states:StartExecution"
                ],
                resources=[opening_nights_table.table_arn,
                           feed_table.table_arn,
                           feed_step_function.state_machine_arn
                        ]
            )
        )

        read_feed_sqs_lambda = create_lambda_function(
            "readFeedSqs",
            "read_feed_sqs.read",
            "lambdas/readFeedSqs",
            "",
            [],
            feed_lambda_role,
            feed_step_function.state_machine_arn
        )
        feed_queue.grant_consume_messages(read_feed_sqs_lambda)
        read_feed_sqs_lambda.add_event_source(eventsources.SqsEventSource(feed_queue))

        feed_queue.grant_send_messages(update_subscriptions_lambda)
        feed_queue.grant_send_messages(rate_film_lambda)

        #API Gateway
        opening_nights_api = apigateway.RestApi(self, "Opening-Night-Api",
            default_cors_preflight_options={
                "allow_origins": apigateway.Cors.ALL_ORIGINS,
                "allow_methods": apigateway.Cors.ALL_METHODS,
                "allow_headers": ["Content-Type", "X-Amz-Date", "Authorization", "X-Api-Key"],
                "status_code": 200
            })

        opening_nights_api.root.add_method("ANY")

        films = opening_nights_api.root.add_resource("films")
        upload_film_integration = apigateway.LambdaIntegration(upload_film_lambda)
        films.add_method("POST", upload_film_integration)
        get_all_films_integration = apigateway.LambdaIntegration(get_all_films_lambda)
        films.add_method("GET", get_all_films_integration)

        film = opening_nights_api.root.add_resource("{name}")
        download_film_integration = apigateway.LambdaIntegration(download_film_lambda)
        film.add_method("GET", download_film_integration)

        film_by_id = films.add_resource("{id}")
        get_film_by_id_integration = apigateway.LambdaIntegration(get_film_by_id_lambda)
        film_by_id.add_method("GET", get_film_by_id_integration)

        film_update = opening_nights_api.root.add_resource('update').add_resource("{id}")
        get_film_by_id_update_integration = apigateway.LambdaIntegration(get_film_by_id_update_lambda)
        film_update.add_method("GET", get_film_by_id_update_integration)

        update_film_integration = apigateway.LambdaIntegration(update_film_lambda)
        films.add_method("PUT", update_film_integration)

        subs_resource = opening_nights_api.root.add_resource('subscriptions')
        subs = subs_resource.add_resource("{username}")
        
        update_subscriptions_integration = apigateway.LambdaIntegration(update_subscriptions_lambda,
                                                                        request_templates={'application/json': '{"statusCode": 200}'})
        subs.add_method("POST", update_subscriptions_integration)

        get_subscriptions_integration = apigateway.LambdaIntegration(get_subscriptions_lambda)
        subs.add_method("GET", get_subscriptions_integration)

        actors_and_directors = opening_nights_api.root.add_resource("actors-and-directors")
        get_actors_and_directors_integration = apigateway.LambdaIntegration(get_actors_and_directors_lambda)
        actors_and_directors.add_method("GET", get_actors_and_directors_integration)

        series_resource = films.add_resource("series")
        get_series_list_integration = apigateway.LambdaIntegration(get_series_list_lambda)
        series_resource.add_method("GET", get_series_list_integration)

        series_episodes_resource = series_resource.add_resource("{seriesName}").add_resource("episodes")
        get_episodes_by_series_integration = apigateway.LambdaIntegration(get_episodes_by_series_lambda)
        series_episodes_resource.add_method("GET", get_episodes_by_series_integration)

        ratings = opening_nights_api.root.add_resource("ratings")
        rate_film_integration = apigateway.LambdaIntegration(rate_film_lambda)
        ratings.add_method("POST", rate_film_integration)

        film_ratings = ratings.add_resource("{filmId}")
        get_ratings_for_film_integration = apigateway.LambdaIntegration(get_ratings_for_film_lambda)
        film_ratings.add_method("GET", get_ratings_for_film_integration)
        
        login = opening_nights_api.root.add_resource("login")
        login_integration = apigateway.LambdaIntegration(login_lambda)
        login.add_method("POST", login_integration)

        register = opening_nights_api.root.add_resource("register")
        register_integration = apigateway.LambdaIntegration(register_lambda)
        register.add_method("POST", register_integration)

        feed = opening_nights_api.root.add_resource("feed").add_resource("{username}")
        get_feed_integration = apigateway.LambdaIntegration(get_feed_lambda)
        feed.add_method("GET", get_feed_integration)

