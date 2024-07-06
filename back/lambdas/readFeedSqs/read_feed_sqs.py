import json
import os
import boto3

sfn_client = boto3.client('stepfunctions')

def read(event, context):
    state_machine_arn = os.environ['CUSTOM_VAR']
    for record in event['Records']:
        username = record['body']

        response = sfn_client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps({"username": username})
        )
        print(response)