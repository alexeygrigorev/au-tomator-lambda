import os
import json
import base64
import requests


SLACK_TOKEN = os.getenv('SLACK_TOKEN')

headers = {
    'Authorization': f'Bearer {SLACK_TOKEN}'
}


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



def post_message_thread(event, message):
    item = event['item']
    channel = item['channel']
    thread_ts = item['ts']
    
    url = 'https://slack.com/api/chat.postMessage'

    message = {
        "channel": channel,
        "thread_ts": thread_ts,
        "blocks": [{
            "type": "section",
            "text": {"type": "mrkdwn", "text": message}
        }]
    }

    response = requests.post(url, json=message, headers=headers).json()
    
    

def default_action(body, event):
    print('default_action')
    print(json.dumps(body))
    print()


def dont_ask_to_ask(body, event):
    message = "Don't ask to ask:\nhttps://dontasktoask.com/"
    post_message_thread(event, message)


def thread(body, event):
    message = (
        "Please reply in threads to keep the discussion more organized:\n" + 
        "https://datatalks.club/slack/guidelines.html#taking-part-in-discussions"
    )
    post_message_thread(event, message)    


admins = {'U01AXE0P5M3'}

reaction_actions = {
    'dont-ask-to-ask-just-ask': dont_ask_to_ask,
    'thread': thread,
}

def lambda_handler(event, context):
    print(json.dumps(event))

    body = extract_body(event)
    print(json.dumps(body))

    if 'challenge' in body:
        return challenge(body)

    event = body['event']
    user = event['user']
    event_type = event['type']    
    print(f'user: {user} (admin: {user in admins}), event_type: {event_type}')

    if (event_type == 'reaction_added') and (user in admins):
        reaction = event['reaction']
        action = reaction_actions.get(reaction, default_action)
        print(f'reaction: {reaction}, action: {action}')
        action(body, event)

    return {
        'statusCode': 200,
        'body': "Hello from lambda!"
    }
