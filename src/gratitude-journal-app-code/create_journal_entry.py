import json
import boto3
import os
import ulid

table_name = os.environ['GRATITUDE_JOURNAL_DDB_TABLE']


def bad_request(message):
    response_code = 400
    response_body = {'feedback': message}
    response = {'statusCode': response_code,
                'headers': {'x-custom-header': 'custom-header'},
                'body': json.dumps(response_body)}
    return response


def lambda_handler(event, context):
    response_code = 200
    print("request: " + json.dumps(event))
    if 'body' not in event:
        return bad_request('you have to include a request body')
    body = json.loads(event['body'])
    if 'entry' not in body:
        return bad_request('the request body has to include an entry')

    entry_content = event['body']['entry']
    dynamodb_client = boto3.client('dynamodb')

    entry_ulid = str(ulid.new())

    response = dynamodb_client.put_item(
        TableName=table_name,
        Item={
            'PK1': {'S': 'ENTRY'},
            'SK1': {'S': f'ENTRY_ID#{entry_ulid}'},
            'ENTRY_CONTENT': {'S': entry_content}
        }
    )

    response_body = {
        'message': 'Entry received!',
        'input': event
    }

    response = {
        'statusCode': response_code,
        'headers': {
            'x-custom-header': 'custom header'
        },
        'body': json.dumps(response_body)
    }
    print("response: " + json.dumps(response))
    return response
