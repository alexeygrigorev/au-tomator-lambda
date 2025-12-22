import os
import json

import yaml

import util
import groqu
import slack
from logs import logger


FAKE_DELETE = os.getenv('FAKE_DELETE', '0') == '1'
CONFIG_FILE = os.getenv('CONFIG_FILE', 'config.yaml')



with open(CONFIG_FILE, 'r') as f_in:
    config = yaml.safe_load(f_in)


reaction_configs = {}

for c in config['reactions']:
    reaction = c['reaction']
    reaction_configs[reaction] = c


def get_channel_name(channel_id):
    return config['channels'].get(channel_id, None)
    

def handle_slack_post(event, reaction_config):
    channel_id = event['item']['channel']
    channel_name = get_channel_name(channel_id)

    if 'placeholders' in reaction_config:
        message = util.format_message(
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
    message_pattern = reaction_config['message']

    item = event['item']
    channel = item['channel']
    ts = item['ts']

    message_details = slack.get_message_content(channel, ts)
    user = message_details['user']
    original_message = message_details['text']

    values = {
        'user': user,
        'user_message': original_message,
        'channel': channel,
    }

    if 'placeholders' in reaction_config:
        values.update(reaction_config['placeholders'])

    message_dm = util.format_message(message_pattern, values, channel)

    slack.send_dm(user, message_dm)

    if FAKE_DELETE:
        logger.info(f"FAKE_DELETE for {channel} {ts}")
    else:
        slack.remove_message(channel, ts)


def handle_ask_ai(event, reaction_config):
    user, original_message = slack.get_message(event)

    prompt = reaction_config['prompt_template'].format(user_message=original_message)
    model = reaction_config['model']

    ai_response = groqu.ai_request(prompt, model)
    ai_response = slack.github_to_slack_markdown(ai_response)

    logger.info("response from GROQ: " + ai_response)

    message = reaction_config['answer_template'].format(user=user, ai_response=ai_response)

    slack.post_message_thread(event, message)


def handle_delete_with_threads(event, reaction_config):
    """Delete a message and all its thread replies, sending DMs to all affected users"""
    item = event['item']
    channel = item['channel']
    ts = item['ts']
    
    # Get parent message details
    parent_message = slack.get_message_content(channel, ts)
    parent_user = parent_message['user']
    parent_text = parent_message['text']
    
    # Get thread replies
    thread_replies = slack.get_thread_replies(channel, ts)
    
    # Delete all thread replies first
    thread_message_pattern = reaction_config.get('thread_message', '')
    for reply in thread_replies:
        reply_user = reply.get('user')
        reply_ts = reply['ts']
        
        if reply_user:  # Only process messages with a user (not bot messages)
            # Send DM to thread reply author
            thread_values = {
                'user': reply_user,
                'channel': channel,
            }
            
            if 'placeholders' in reaction_config:
                thread_values.update(reaction_config['placeholders'])
            
            thread_dm = util.format_message(thread_message_pattern, thread_values, channel)
            
            if thread_dm:
                slack.send_dm(reply_user, thread_dm)
            
            # Delete the thread reply
            if FAKE_DELETE:
                logger.info(f"FAKE_DELETE thread reply for {channel} {reply_ts}")
            else:
                slack.remove_message(channel, reply_ts)
    
    # Now handle the parent message
    parent_message_pattern = reaction_config['message']
    
    parent_values = {
        'user': parent_user,
        'user_message': parent_text,
        'channel': channel,
    }
    
    if 'placeholders' in reaction_config:
        parent_values.update(reaction_config['placeholders'])
    
    parent_dm = util.format_message(parent_message_pattern, parent_values, channel)
    
    if parent_dm:
        slack.send_dm(parent_user, parent_dm)
    
    # Delete the parent message
    if FAKE_DELETE:
        logger.info(f"FAKE_DELETE parent message for {channel} {ts}")
    else:
        slack.remove_message(channel, ts)


action_handlers = {
    'SLACK_POST': handle_slack_post,
    'DELETE_MESSAGE': handle_delete_message,
    'DELETE_WITH_THREADS': handle_delete_with_threads,
    'ASK_AI': handle_ask_ai,
}


def process_reaction(body, event):
    reaction = event['reaction']

    if reaction not in reaction_configs:
        logger.info(f"no reaction config for {reaction}")
        return

    reaction_config = reaction_configs[reaction]

    action_type = reaction_config['type']
    action_handler = action_handlers.get(action_type)
    
    if action_handler:
        action_handler(event, reaction_config)
    else:
        logger.info(f"no handler for {action_type}")


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