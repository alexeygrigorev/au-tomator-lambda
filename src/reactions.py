import os
import json
from typing import Dict, Set

import yaml

import slack


class EmojiAction:

    ACTION_TYPE = 'NOOP'

    def react(self, body, event):
        print('default_action')
        print(json.dumps(body))
        print()

    @classmethod
    def build(cls, reaction) -> EmojiAction:
        assert reaction['type'] == cls.ACTION_TYPE
        return EmojiAction()


class SendMessageEmojiAction(EmojiAction):

    ACTION_TYPE = 'SLACK_POST'

    def __init__(self, message) -> None:
        super().__init__()
        self.message = message

    def react(self, body, event):
        slack.post_message_to_thread(event, self.message)

    @classmethod
    def build(cls, reaction) -> EmojiAction:
        assert reaction['type'] == cls.ACTION_TYPE
        message = reaction['message']
        return SendMessageEmojiAction(message)



class SendMessageChannelAwareEmojiAction(EmojiAction):

    ACTION_TYPE = 'SLACK_POST_CHANNEL_AWARE'

    def __init__(self) -> None:
        super().__init__()

    def react(self, body, event):
        #SLACK_POST_CHANNEL_AWARE
        pass

    @classmethod
    def build(cls, reaction) -> EmojiAction:
        assert reaction['type'] == cls.ACTION_TYPE
        print('no op yet')
        return SendMessageChannelAwareEmojiAction()


def find_action_classes():
    for v in globals():
        try: 
            if issubclass(v, EmojiAction):
                yield v
        except TypeError:
            pass


def build_action_index(): 
    reaction_classes = find_action_classes()
    index = {}

    for ActionClass in reaction_classes:
        index[ActionClass.ACTION_TYPE] = ActionClass.build

    return index



class ReactionsApp:

    def __init__(self,
        admins: Set[str],
        channels: Dict[str, str],
        actions: Dict[str, EmojiAction],
        default_action: EmojiAction,
    ) -> None:
        self.admins = admins
        self.channels = channels
        self.actions = actions
        self.default_action = default_action

    def react(self, body, event):
        user = event['user']
        if user not in self.admins:
            return 200, 'not reacting'

        reaction = event['reaction']


        status_code = 200
        body = 'ok'

        return status_code, body



def parse_config(config) -> ReactionsApp:
    admins = set(config['admins'])
    channels = config['channels']

    action_class_index = build_action_index()

    actions = {}
    for reaction_name, reaction in config['reactions']:
        reaction_type = reaction['type']
        reaction_builder = action_class_index[reaction_type]
        actions[reaction_name] = reaction_builder(reaction)

    default_action = EmojiAction()

    return ReactionsApp(
        admins=admins,
        channels=channels,
        actions=actions,
        default_action=default_action
    )


def build_from(yaml_file: str) -> ReactionsApp:
    with open(yaml_file, 'rt') as f_in:
        config = yaml.load(yaml_file)
        return parse_config(config)


def build_default() -> ReactionsApp:
    CONFIG_FILE = os.getenv('CONFIG_FILE', 'config.json')
    return build_from(CONFIG_FILE)