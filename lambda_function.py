import json
import base64


def extract_body(event):
    if 'body' not in event:
        return {}
    
    raw = event['body']
    
    base64_needed = event.get('isBase64Encoded', False)
    if base64_needed:
        raw = base64.b64decode(encoded_data).decode('utf-8')

    decoded = json.loads(raw)
    return decoded


def challenge(body):
    print(json.dumps(body))

    challenge_answer = body.get("challenge")
    
    return {
        'statusCode': 200,
        'body': challenge_answer
    }


def lambda_handler(event, context):
    print(json.dumps(event))

    body = extract_body(event)

    if 'challenge' in body:
        return challenge(body)

    print(json.dumps(body))

    return {
        'statusCode': 200,
        'body': "Hello from lambda!"
    }
