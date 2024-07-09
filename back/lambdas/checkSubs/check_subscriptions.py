import os
import boto3

dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')
sns = boto3.client('sns')

def check(event, context):

    table_name = os.environ['SUBS_TABLE_NAME']
    table = dynamodb.Table(table_name)
    data = table.scan()
    subs = data['Items']

    for record in event['Records']:
        if record['eventName'] not in ['INSERT', 'MODIFY']:
            continue

        print(record)
        new_image = record['dynamodb']['NewImage']
        title = new_image.get('title', '').get('S', '')
        genres = new_image.get('genres', {}).get('L', [])
        for g in genres:
            genre = g.get('S', '')
            print(g)
            message = f'A new {genre} film "{title}" just arrived!'
            pub('g' + genre, message)

        directors = new_image.get('directors', {}).get('L', [])
        for d in directors:
            print(d)
            director = d.get('S', '')
            message = f'A new film "{title}" by {director} just arrived!'
            pub('d' + director, message)

        actors = new_image.get('actors', {}).get('L', [])
        for a in actors:
            print(a)
            actor = a.get('S', '')
            message = f'A new film "{title}" starring {actor} just arrived!'
            pub('a' + actor, message)

        #writes to sqs
        for sub in subs:
            found_intersection = False
            for g in genres:
                genre = g.get('S', '')
                if genre in sub['genres']:
                    found_intersection = True
                    break
            for d in directors:
                director = d.get('S', '')
                if director in sub['directors']:
                    found_intersection = True
                    break
            for a in actors:
                actor = a.get('S', '')
                if actor in sub['actors']:
                    found_intersection = True
                    break
            if found_intersection:
                queue_url = os.environ['CUSTOM_VAR']
                sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody=sub['username']
                )



def pub(topic_name, message):
    topic_name = topic_name.replace(' ', '_')
    print(topic_name)
    response = sns.create_topic(Name=topic_name)
    topic_arn = response['TopicArn']

    sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject="Film library updated"
    )