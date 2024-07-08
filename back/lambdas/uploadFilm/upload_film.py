from io import BytesIO
import json
import os
import boto3
import base64
from datetime import datetime
import uuid
import tempfile
import subprocess

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def transcode_video(input_bytes, film_id):
    # Write input bytes to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_input:
        temp_input.write(input_bytes)
        temp_input_path = temp_input.name
    
    output_360p_path = film_id + "_360p.mp4"
    output_144p_path = film_id + "_144p.mp4"

    command = [
            'ffmpeg',
            '-i', temp_input_path,
            '-vf', f'scale={256}:{144}',
            '-c:a', 'copy',
            output_360p_path
        ]

    subprocess.run(command, check=True)

    command = [
            'ffmpeg',
            '-i', temp_input_path,
            '-vf', f'scale={480}:{360}',
            '-c:a', 'copy',
            output_144p_path
        ]

    subprocess.run(command, check=True)

    # Read the transcoded videos back into bytes
    with open(output_360p_path, 'rb') as f:
        output_360p_bytes = f.read()

    with open(output_144p_path, 'rb') as f:
        output_144p_bytes = f.read()

    # Clean up temporary files
    os.remove(temp_input_path)
    os.remove(output_360p_path)
    os.remove(output_144p_path)

    return output_360p_bytes, output_144p_bytes

def create(event, context):
    body = json.loads(event['body'])

    film_id = str(uuid.uuid4())
    file_name = body['fileName']
    file_content = base64.b64decode(body['fileContent'])

    bucket_name = os.environ['BUCKET_NAME']
    s3_client.put_object(
        Bucket=bucket_name,
        Key=film_id,
        Body=file_content,
        ContentType='video/mp4',
        Metadata={
            'Name': file_name,
            'Type': 'video/mp4',
            'Size': f"{len(file_content)}B",
            'Time created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Last modified': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
    )

    output_360p_bytes, output_144p_bytes = transcode_video(file_content, film_id)

    filename_360p = file_name.replace(".mp4", "_360p.mp4")
    file_id_360p = film_id + "_360p"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_id_360p,
        Body=output_360p_bytes,
        ContentType='video/mp4',
        Metadata={
            'Name': filename_360p,
            'Type': 'video/mp4',
            'Size': f"{len(output_360p_bytes)}B",
            'Time created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Last modified': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
    )

    filename_144p = file_name.replace(".mp4", "_144p.mp4")
    file_id_144p = film_id + "_144p"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_id_144p,
        Body=output_144p_bytes,
        ContentType='video/mp4',
        Metadata={
            'Name': filename_144p,
            'Type': 'video/mp4',
            'Size': f"{len(output_144p_bytes)}B",
            'Time created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Last modified': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
    )

    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)
    table.put_item(
        Item = {
                'filmId': film_id,
                'fileName': body['fileName'],
                'title' : body['title'],
                'description' : body['description'],
                'actors' : body['actors'],
                'directors' : body['directors'],
                'genres' : body['genres'],
                'isSeries': body['isSeries'],
                'series': body.get('series', None) # Optional field
            }
    )

    message = {
        'message': 'Successfully uploaded film'
    }

    return { 
            'statusCode': 200, 
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(message, default=str)
            }
