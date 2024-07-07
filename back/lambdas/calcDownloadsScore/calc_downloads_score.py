import os
import boto3
from datetime import datetime

import boto3.dynamodb
import boto3.dynamodb.conditions

dynamodb = boto3.resource('dynamodb')

def calc_downloads_score(event, context):
    
    username = event['username']

    table_name = os.environ['DOWNLOADS_TABLE_NAME']
    table = dynamodb.Table(table_name)

    directors = {}
    actors = {}
    genres = {}
    downloaded_films = []

    items = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('username').eq(username)
    )
    try:
        downloads = items['Items']

    except (KeyError):
        print('username not found error (no item found)')
        downloads = []

    for download in downloads:
        # timestamp effect => 1, 0.75, 0.5, 0.25, 0, for delta t: 0-7, 8-14, 15-28, 29-56, 57-inf
        score = 1
        dt = (datetime.now() - datetime.fromisoformat(download['timestamp'])).days
        cont = True
        limit = 7
        while cont and score > 0:
            if dt <= limit:
                cont = False
                break
            score -= 0.25
            limit *= 2

        if (score == 0):
            continue

        downloaded_films.append(download['filmId'])
        directors_list = download['directors']
        for d in directors_list:
            try:
                directors[d].append(score)
            except (KeyError):
                directors[d] = [score]

        actors_list = download['actors']
        for a in actors_list:
            try:
                actors[a].append(score)
            except (KeyError):
                actors[a] = [score]

        genres_list = download['genres']
        for g in genres_list:
            try:
                genres[g].append(score)
            except (KeyError):
                genres[g] = [score]

    for d in directors.keys():
        directors[d] = sum(directors[d]) / len(directors[d])

    for a in actors.keys():
        actors[a] = sum(actors[a]) / len(actors[a])
        
    for d in genres.keys():
        genres[d] = sum(genres[d]) / len(genres[d])

    response = {
            'downloads_genres': genres,
            'downloads_directors': directors,
            'downloads_actors': actors,
            'downloaded_films': downloaded_films
            }
    return {'Download': response}

