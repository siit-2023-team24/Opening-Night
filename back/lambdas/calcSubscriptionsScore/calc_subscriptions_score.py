import os
import boto3

dynamodb = boto3.resource('dynamodb')

def calc_subs_score(event, context):

    CONST = 1

    username = event['username']

    table_name = os.environ['SUBS_TABLE_NAME']
    table = dynamodb.Table(table_name)
    
    subs = table.get_item(Key={'username': username})

    directors = {}
    actors = {}
    genres = {}
    try:    
        item = subs['Item']
        directors_list = item['directors']
        for d in directors_list:
            directors[d] = CONST
        actors_list = item['actors']
        for a in actors_list:
            actors[a] = CONST
        genres_list = item['genres']
        for g in genres_list:
            genres[g] = CONST
    except (KeyError):
        print('username not found error (no item found)')

    response = {
            'subs_genres': genres,
            'subs_directors': directors,
            'subs_actors': actors,
            'username': username
            }
    return {'Subs': response}
    