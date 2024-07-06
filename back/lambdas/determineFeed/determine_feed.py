import os
import boto3
import json
from bisect import insort

dynamodb = boto3.resource('dynamodb')

def determine_feed(event, context):

    event_downloads = event['Download']
    event_ratings = event['Rating']
    event_subs = event['Subs']
    username = event_subs['username']

    #joining the results
    director_scores = event_ratings['ratings_directors']
    for d, score in event_subs['subs_directors'].items():
        try:
            director_scores[d] += score
        except KeyError:
            director_scores[d] = score
    for d, score in event_downloads['downloads_directors'].items():
        try:
            director_scores[d] += score
        except KeyError:
            director_scores[d] = score

    genre_scores = event_ratings['ratings_genres']
    for g, score in event_subs['subs_genres'].items():
        try:
            genre_scores[g] += score
        except KeyError:
            genre_scores[g] = score
    for g, score in event_downloads['downloads_genres'].items():
        try:
            genre_scores[g] += score
        except KeyError:
            genre_scores[g] = score

    actor_scores = event_ratings['ratings_actors']
    for a, score in event_subs['subs_actors'].items():
        try:
            actor_scores[a] += score
        except KeyError:
            actor_scores[a] = score
    for a, score in event_downloads['downloads_actors'].items():
        try:
            actor_scores[a] += score
        except KeyError:
            actor_scores[a] = score
    
    max_len = 5
    feed = []   

    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)

    data = table.scan()
    films = data["Items"]
    for film in films:
        score = 0
        for genre in film['genres']:
            try:
                score += genre_scores[genre]
            except KeyError:
                pass
        for director in film['directors']:
            try:
                score += director_scores[director]
            except KeyError:
                pass
        for actor in film['actors']:
            try:
                score += actor_scores[actor]
            except KeyError:
                pass

        n = len(feed)
        if n < max_len or (n > 0 and feed[-1][1] < score):
            feed.append((film, score))
            feed.sort(key=lambda x: x[1], reverse=True)
            if (n+1 > max_len):
                feed = feed[:-1]

    # feed determined, saving to db
    feed_table_name = os.environ['FEED_TABLE_NAME']
    feed_table = dynamodb.Table(feed_table_name)

    feed_table.put_item(
        Item = {
            'username': username,
            'films': feed
        }
    )
    print('Feed updated for ' + username + ': ', feed)