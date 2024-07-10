import os
import json

import yaml
import requests

import slack
from logs import logger


FAKE_DELETE = os.getenv('FAKE_DELETE', '0') == '1'
CONFIG_FILE = os.getenv('CONFIG_FILE', 'config.yaml')

GROQ_API_KEY = os.getenv('GROQ_API_KEY')


with open(CONFIG_FILE, 'r') as f_in:
    config = yaml.safe_load(f_in)


def send_dm_and_delete(item, message_pattern):
    channel = item['channel']
    ts = item['ts']

    message_details = slack.get_message_content(channel, ts)
    user = message_details['user']
    message_text = message_details['text']

    message_dm = message_pattern.format(
        user=user,
        channel=channel,
        message_text=message_text
    )

    slack.send_dm(user, message_dm)

    if FAKE_DELETE:
        logger.info(f"FAKE_DELETE for {channel} {ts}")
    else:
        slack.remove_message(channel, ts)
    


def get_message(event):
    item = event['item']
    channel = item['channel']
    ts = item['ts']

    message_details = slack.get_message_content(channel, ts)

    user = message_details['user']
    message_text = message_details['text']

    return user, message_text


def groq_request(prompt, model):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}'
    }

    ai_request = {
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "model": model,
    }

    response = requests.post(url, json=ai_request, headers=headers)
    response.raise_for_status()
    
    chat_completion = response.json()
    ai_response = chat_completion['choices'][0]['message']['content']
    
    return ai_response


def ask_ai(event, reaction_config):
    user, original_message = get_message(event)

    prompt = reaction_config['prompt_template'].format(user_message=original_message)
    model = reaction_config['model']

    ai_response = groq_request(prompt, model)
    ai_response = slack.github_to_slack_markdown(ai_response)

    logger.info("response from GROQ: " + ai_response)

    message = reaction_config['answer_template'].format(user=user, ai_response=ai_response)

    slack.post_message_thread(event, message)


def get_channel_name(channel_id):
    return config['channels'].get(channel_id, None)


def format_message_with_placeholders(message_template, placeholders, channel_name):
    # TODO: refactor, the logic is not clear
    for key, value in placeholders.items():
        if isinstance(value, dict):
            default_value = value.get('default', None)
            placeholder_value = value.get(channel_name, default_value)
            if placeholder_value is None:
                return None
        else:
            placeholder_value = value
        message_template = message_template.replace(f'{{{key}}}', placeholder_value)
    return message_template


def handle_slack_post(event, reaction_config):
    channel_id = event['item']['channel']
    channel_name = get_channel_name(channel_id)

    if 'placeholders' in reaction_config:
        message = format_message_with_placeholders(
            reaction_config['message'],
            reaction_config['placeholders'],
            channel_name
        )
        if message is None:
            return
    else:
        message = reaction_config['message']
    
    slack.post_message_thread(event, message)


def handle_delete_message(event, reaction_config):
    message = reaction_config['message']
    send_dm_and_delete(event['item'], message)


action_handlers = {
    'SLACK_POST': handle_slack_post,
    'DELETE_MESSAGE': handle_delete_message,
    'ASK_AI': ask_ai,
}


def process_reaction(body, event):
    reaction = event['reaction']

    for reaction_config in config['reactions']:
        if reaction_config['reaction'] == reaction:
            action_type = reaction_config['type']
            action_handler = action_handlers.get(action_type)
            
            if action_handler:
                action_handler(event, reaction_config)
            break


def run(body):
    print(json.dumps(body))
    event = body['event']
    logger.info(f'reaction: {event["reaction"]}')
    process_reaction(body, event)


def lambda_handler(event, context):
    run(event)
    return {
        'statusCode': 200,
        'body': "done"
    }