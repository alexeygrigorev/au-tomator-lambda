import os
import json
import base64
import requests

from logs import logger

SLACK_TOKEN = os.getenv('SLACK_TOKEN')
USER_SLACK_TOKEN = os.getenv('USER_SLACK_TOKEN')


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


def post_message_thread(event, message):
    item = event['item']
    channel = item['channel']
    thread_ts = item['ts']
    
    url = 'https://slack.com/api/chat.postMessage'

    message_request = {
        "channel": channel,
        "thread_ts": thread_ts,
        "blocks": [{
            "type": "section",
            "text": {"type": "mrkdwn", "text": message}
        }]
    }

    headers = {
        'Authorization': f'Bearer {SLACK_TOKEN}'
    }

    logger.info(f'posting {message} to {channel}...')
    response = requests.post(url, json=message_request, headers=headers)
    response.raise_for_status()

    response_json = response.json()
    print(json.dumps(response_json))

    return response_json


def find_message_by_ts(messages, ts):
    for msg in messages:
        if msg['ts'] == ts:
            return msg
    return None


def get_message_content(channel, ts):
    params = {
        'channel': channel,
        'lastest': ts,
        'limit': 10,
        'inclusive': True
    }

    headers = {
        'Authorization': f'Bearer {SLACK_TOKEN}'
    }

    url = 'https://slack.com/api/conversations.history'
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    
    response_json = response.json()
    # print(json.dumps(response_json))
    message = find_message_by_ts(response_json['messages'], ts)
    return message


def send_dm(user, message):    
    url = 'https://slack.com/api/chat.postMessage'

    message_request = {
        "channel": user,
        "blocks": [{
            "type": "section",
            "text": {"type": "mrkdwn", "text": message}
        }]
    }

    headers = {
        'Authorization': f'Bearer {SLACK_TOKEN}'
    }
    
    logger.info(f'posting {message} to {user}...')
    response = requests.post(url, json=message_request, headers=headers)
    response.raise_for_status()
    return response.json()


def remove_message(channel, ts):
    url = 'https://slack.com/api/chat.delete'

    message_request = {
        "channel": channel,
        "ts": ts
    }
    
    headers = {
        'Authorization': f'Bearer {USER_SLACK_TOKEN}'
    }

    logger.info(f'removing message from {channel} at {ts}...')
    response = requests.post(url, json=message_request, headers=headers)
    response.raise_for_status()
    return response.json()


def get_user_and_message(event):
    item = event['item']
    channel = item['channel']
    ts = item['ts']

    message_details = get_message_content(channel, ts)

    user = message_details['user']
    message_text = message_details['text']

    return user, message_text
