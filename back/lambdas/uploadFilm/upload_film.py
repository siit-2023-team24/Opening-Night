import json
import os
import boto3

sfn_client = boto3.client('stepfunctions')

def upload(event, context):
    state_machine_arn = os.environ['CUSTOM_VAR']

    sfn_client.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps(event)
    )
