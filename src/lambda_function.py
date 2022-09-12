import json
import base64
import reactions


reactions_app = reactions.build_default()


def extract_body(event):
    if 'body' not in event:
        return {}

    raw = event['body']

    base64_needed = event.get('isBase64Encoded', False)
    if base64_needed:
        raw = base64.b64decode(raw).decode('utf-8')

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
    print(json.dumps(body))

    if 'challenge' in body:
        return challenge(body)

    slack_event = body['event']
    event_type = slack_event['type']
    print(f'{event_type=}, {slack_event=}')

    if event_type == 'reaction_added':
        status_code, body = reactions_app.react(body, slack_event)
    else:
        status_code, body = (200, 'ok')

    return {
        'statusCode': status_code,
        'body': body
    }
