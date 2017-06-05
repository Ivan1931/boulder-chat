import sys
from . import store
from . import client
from . import authserver as a
from . import crypto as c

def select_option(options):
    selected = len(options)
    while selected < 0 or len(option) <= selected:
        try:
            selected = int(sys.stdin.readline())
            if selected < 0 or len(option) <= selected:
                print(f'Please select a number between 0 and {len(option)}')
        except ValueError(e):
            print('Please enter a number')
            selected = len(option)
    return option[selected]

help_message = """
Usage:
    conv - view a conversation
    chat - send a message to existing contact
    first - send a message to a new contact
"""
def main():
    store = store.ClientStore()
    chatting = True
    while chatting:
        line = sys.stdin.readline()
        if line == "chat":
            options = []
            for option, user in enumerate(store.all_user_data()):
                print(f"[{option}] Public Key:\n{user}")
                options.append(user)
            user = select_option(options)
            send_message(store, user, message)
        elif line == "conv":
            options = []
            for option, user in enumerate(store.all_user_data()):
                print(f"[{option}] Public Key:\n{user}")
                options.append(user)
            user = select_option(options)
            conversation = store.get_user_conversation(user)
            for message in conversation:
                display = ''
                if message['sender']:
                    display += '[US] '
                else:
                    display += '[THEM] '
                if message['is_file']:
                    display += message['file_path']
                else:
                    display += message['message']
                print(display)
        elif line == 'first':
            pass
        else:
            print(help_message)


            
             

