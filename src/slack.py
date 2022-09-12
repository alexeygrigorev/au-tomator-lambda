import os
import json
import requests


SLACK_TOKEN = os.getenv('SLACK_TOKEN')


def post_message_to_thread(event, message):
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

    print(f'posting {message} to {channel}...')
    response = requests.post(url, json=message_request, headers=headers).json()
    print(json.dumps(response))