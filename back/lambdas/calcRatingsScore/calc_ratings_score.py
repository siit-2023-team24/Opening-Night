import os
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

def calc_ratings_score(event, context):

    username = event['username']

    table_name = os.environ['RATINGS_TABLE_NAME']
    table = dynamodb.Table(table_name)

    items = table.query(
        IndexName='username-index',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('username').eq(username)
    )
    ratings = items['Items']

    directors = {}
    actors = {}
    genres = {}

    for rating in ratings:

        # timestamp effect => 1, 0.75, 0.5, 0.25, 0, for delta t: 0-7, 8-14, 15-28, 29-56, 57-inf
        time_score = 1
        dt = (datetime.now() - datetime.fromisoformat(rating['timestamp'])).days
        cont = True
        limit = 7
        while cont and time_score > 0:
            if dt <= limit:
                cont = False
                break
            time_score -= 0.25
            limit *= 2

        if (time_score == 0):
            continue

        # rating score: 1 = -1, 2 = 0.25, 3 = 0.5, 4 = 0.75, 5 = 1
        rating['stars'] = int(rating['stars'])
        score = (rating['stars'] - 1)
        if (score == 0): 
            score = -1
        else:
            score *= 0.25

        score *= time_score
  
        directors_list = rating['directors']
        for d in directors_list:
            if (d not in directors):
                directors[d] = []
            directors[d].append(score)

        actors_list = rating['actors']
        for a in actors_list:
            if (a not in actors):
                actors[a] = []
            actors[a].append(score)

        genres_list = rating['genres']
        for g in genres_list:
            if (g not in genres):
                genres[g] = []
            genres[g].append(score)

    for d in directors.keys():
        directors[d] = sum(directors[d]) / len(directors[d])

    for a in actors.keys():
        actors[a] = sum(actors[a]) / len(actors[a])
        
    for d in genres.keys():
        genres[d] = sum(genres[d]) / len(genres[d])

    response = {
            'ratings_genres': genres,
            'ratings_directors': directors,
            'ratings_actors': actors
            }
    return {'Rating': response}
