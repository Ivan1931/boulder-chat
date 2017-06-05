import sys
from . import store
from . import client
from . import authserver as a
from . import crypto as c

def read_line():
    return sys.stdin.readline().strip()

def select_option(options):
    selected = len(options)
    if len(options) == 0:
        print("It seems like there are no options to select from")
        return
    while selected < 0 or len(options) <= selected:
        try:
            selected = int(read_line())
            if selected < 0 or len(options) <= selected:
                print(f'Please select a number between 0 and {len(option)}')
        except ValueError:
            print('Please enter a number')
            selected = len(options)
    return options[selected]

help_message = """
Usage:
    conv - view a conversation
    chat - send a message to existing contact
    first - send a message to a new contact
"""
def main():
    store = client.get_sender()
    chatting = True
    print("Welcome to boulder chat")
    while chatting:
        print(help_message)
        line = read_line()
        if line == "chat":
            options = []
            for option, user in enumerate(store.all_user_data()):
                print(f"[{option}] Public Key:\n{user}")
                options.append(user)
            reciever_public_key = select_option(options)
            if reciever_public_key:
                client.deliver_message(store, reciever_public_key, read_line())
        elif line == "conv":
            options = []
            for option, user in enumerate(store.all_user_data()):
                print(f"[{option}] Public Key:\n{user}")
                options.append(user)
            user = select_option(options)
            if user:
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
            print("Please provide a path to a PEM file of their public key")
            file_path = read_line()
            with open(file_path, 'rb') as f:
                contents = f.read()
            print(contents)
            try:
                reciever_public_key = c.import_public_key(contents)
            except:
                print("File you specified does not seem to be a public key file")
                continue
            print("Now enter the domain name of the other user")
            host = read_line()
            print("Please enter the message you would like to send")
            message = read_line()
            client.deliver_first_message(store, host, reciever_public_key, message)
        else:
            print(help_message)


            
if __name__=="__main__":
    main()
