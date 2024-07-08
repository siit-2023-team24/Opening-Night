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
    
    output_360p_path = f"/tmp/{film_id}_360p.mp4"

    command = [
            'ffmpeg',
            '-i', temp_input_path,
            '-vf', f'scale={480}:{360}',
            '-c:a', 'copy',
            output_360p_path
        ]

    subprocess.run(command, check=True)

    # Read the transcoded videos back into bytes
    with open(output_360p_path, 'rb') as f:
        output_360p_bytes = f.read()

    # Clean up temporary files
    os.remove(temp_input_path)
    os.remove(output_360p_path)

    return output_360p_bytes

def create(event, context):
    file_content = event['fileContent']
    film_id = event['filmId']
    file_name = event['fileName']

    file_content = base64.b64decode(file_content)

    output_360p_bytes = transcode_video(file_content, film_id)

    bucket_name = os.environ['BUCKET_NAME']
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
