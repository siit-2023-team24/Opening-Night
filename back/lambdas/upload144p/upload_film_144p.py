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
    
    output_144p_path = f"/tmp/{film_id}_144p.mp4"

    command = [
            'ffmpeg',
            '-i', temp_input_path,
            '-vf', f'scale={256}:{144}',
            '-c:a', 'copy',
            output_144p_path
        ]

    subprocess.run(command, check=True)

    # Read the transcoded videos back into bytes
    with open(output_144p_path, 'rb') as f:
        output_144p_bytes = f.read()

    # Clean up temporary files
    os.remove(temp_input_path)
    os.remove(output_144p_path)

    return output_144p_bytes

def create(event, context):
    file_content = event['fileContent']
    film_id = event['filmId']
    file_name = event['fileName']

    file_content = base64.b64decode(file_content)

    output_144p_bytes = transcode_video(file_content, film_id)

    bucket_name = os.environ['BUCKET_NAME']
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
