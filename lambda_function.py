import os
import json
import base64
import requests


SLACK_TOKEN = os.getenv('SLACK_TOKEN')
USER_SLACK_TOKEN = os.getenv('USER_SLACK_TOKEN')


COURSE_MLOPS_ZOOMCAMP_CHANNEL = "C02R98X7DS9"
COURSE_DATA_ENGINEERING_CHANNEL = "C01FABYF2RG"
COURSE_ML_ZOOMCAMP_CHANNEL = "C0288NJ5XSA"


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

    print(f'posting {message} to {channel}...')
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
    
    print(f'posting {message} to {user}...')
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

    print(f'removing message from {channel} at {ts}...')
    response = requests.post(url, json=message_request, headers=headers)
    response.raise_for_status()
    return response.json()


def default_action(body, event):
    print('default_action')
    print(json.dumps(body))
    print()


def dont_ask_to_ask(body, event):
    message = "Don't ask to ask:\nhttps://dontasktoask.com/"
    post_message_thread(event, message)


def thread(body, event):
    message = (
        "Please use threads to keep the discussion more organized:\n" + 
        "https://datatalks.club/slack/guidelines.html#taking-part-in-discussions"
    )
    post_message_thread(event, message)


def error_log_to_thread_please(body, event):
    channel = event['item']['channel']

    if channel == COURSE_DATA_ENGINEERING_CHANNEL:
        guidelines_link = "https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/asking-questions.md"
    elif channel == COURSE_MLOPS_ZOOMCAMP_CHANNEL:
        guidelines_link = "https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/asking-questions.md"
    elif channel == COURSE_ML_ZOOMCAMP_CHANNEL:
        guidelines_link = "https://github.com/alexeygrigorev/mlbookcamp-code/blob/master/course-zoomcamp/asking-questions.md"
    else:
        guidelines_link = "https://datatalks.club/slack/guidelines.html#code-problems-and-errors"

    message = (
        "Please move the error log from the main message to the thread.\n" +
        "Use code block for formatting the log: https://slack.com/help/articles/202288908-Format-your-messages\n\n" +
        f"Follow <{guidelines_link}|these recommendations> to make it easier to help you."
    )

    post_message_thread(event, message)


def faq(body, event):
    channel = event['item']['channel']

    if channel == COURSE_DATA_ENGINEERING_CHANNEL:
        faq_link = "https://docs.google.com/document/d/19bnYs80DwuUimHM65UV3sylsCn2j1vziPOwzBwQrebw/edit"
    elif channel == COURSE_MLOPS_ZOOMCAMP_CHANNEL:
        faq_link = "https://docs.google.com/document/d/12TlBfhIiKtyBv8RnsoJR6F72bkPDGEvPOItJIxaEzE0/edit"
    elif channel == COURSE_ML_ZOOMCAMP_CHANNEL:
        faq_link = "https://docs.google.com/document/d/1LpPanc33QJJ6BSsyxVg-pWNMplal84TdZtq10naIhD8/edit"

    else:
        print('unknown channel, exiting')
        return

    message = f"Please check the <{faq_link}|FAQ>"
    post_message_thread(event, message)  


def no_screenshot(body, event):
    channel = event['item']['channel']

    if channel == COURSE_DATA_ENGINEERING_CHANNEL:
        guidelines_link = "https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/asking-questions.md"
    elif channel == COURSE_MLOPS_ZOOMCAMP_CHANNEL:
        guidelines_link = "https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/asking-questions.md"
    elif channel == COURSE_ML_ZOOMCAMP_CHANNEL:
        guidelines_link = "https://github.com/alexeygrigorev/mlbookcamp-code/blob/master/course-zoomcamp/asking-questions.md"
    else:
        guidelines_link = "https://datatalks.club/slack/guidelines.html#code-problems-and-errors"

    message = "Please don't post screenshost or pictures of your code, " + \
        "they are very difficult to read. Instead, copy the code and put it " + \
        "in a code block.\n\n" + \
        f"Follow <{guidelines_link}|these recommendations> to make it easier to help you."

    post_message_thread(event, message)


def send_dm_and_delete(item, message_pattern):
    channel = item['channel']
    ts = item['ts']

    message_details = get_message_content(channel, ts)
    user = message_details['user']
    message_text = message_details['text']

    message_dm = message_pattern.format(
        user=user,
        channel=channel,
        message_text=message_text
    )

    send_dm(user, message_dm)
    remove_message(channel, ts)


def shameless_rules(body, event):
    message_template = """
Hi <@{user}>! 

You created this message in <#{channel}>:

> {message_text}

We want to make this community useful for everyone, that's why we ask you to follow
the "shameless channels" template and the rules:

https://alexeygrigorev.notion.site/Shameless-promotion-rules-f565ac6aa2064f7190382f2ffd82c876

Your post was removed from the channel. Please adjust your post.

Apologies for the inconvenience. Thank you!
""".strip()

    item = event['item']
    send_dm_and_delete(item, message_template)



def jobs_rules(body, event):
    message_template = """
Hi <@{user}>! 

You created this message in <#{channel}>:

> {message_text}

We want to make this community useful for everyone, that's why we ask you to follow
the templates and the rules suggested here:

https://alexeygrigorev.notion.site/Jobs-b6ab78b9af504c8dac86413e7404fcfb

Your post was removed from the channel. You're free to make adjustments and post again.

Apologies for the inconvenience. Thank you!
""".strip()

    item = event['item']
    send_dm_and_delete(item, message_template)




admins = {'U01AXE0P5M3'}

reaction_actions = {
    'dont-ask-to-ask-just-ask': dont_ask_to_ask,
    'thread': thread,
    'faq': faq,
    'error-log-to-thread-please': error_log_to_thread_please,
    'no-screenshot': no_screenshot,
    'shameless-rules': shameless_rules,
    'jobs-rules': jobs_rules,
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
