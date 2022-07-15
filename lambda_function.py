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

    print(f'posting {message} to {channel}...')
    response = requests.post(url, json=message_request, headers=headers).json()
    print(json.dumps(response))


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


def faq(body, event):
    channel = event['item']['channel']

    if channel == "C01FABYF2RG":
        faq_link = "https://docs.google.com/document/d/19bnYs80DwuUimHM65UV3sylsCn2j1vziPOwzBwQrebw/edit"
    elif channel == "C02R98X7DS9":
        faq_link = "https://docs.google.com/document/d/12TlBfhIiKtyBv8RnsoJR6F72bkPDGEvPOItJIxaEzE0/edit"
    else:
        print('unknown channel, exiting')
        return

    message = f"Please check the <{faq_link}|FAQ>"
    post_message_thread(event, message)  


admins = {'U01AXE0P5M3'}

reaction_actions = {
    'dont-ask-to-ask-just-ask': dont_ask_to_ask,
    'thread': thread,
    'faq': faq,
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
