import sys
import os
from . import store as s
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
    file - send a file to existing content
    first - send a message to a new contact
"""
def main():
    chatting = True
    print("Welcome to boulder chat")
    while chatting:
        print(help_message)
        line = read_line()
        store = s.ClientStore(os.environ['FILE_PATH'])
        if line == "chat":
            options = []
            for option, user in enumerate(store.all_user_data()):
                print(f"[{option}] Public Key:\n{user}")
                options.append(user)
            reciever_public_key = select_option(options)
            if reciever_public_key:
                message = read_line()
                print("=== Sending message ===")
                response = client.deliver_message(store, reciever_public_key, message)
                if response:
                    if 'error' in response:
                        print("Error!")
                        print(response)
                    else:
                        print("Success!")
                        print(response)
                else:
                    print("Some unknown error occured :(")
        elif line == "file":
            options = []
            for option, user in enumerate(store.all_user_data()):
                print(f"[{option}] Public Key:\n{user}")
                options.append(user)
            reciever_public_key = select_option(options)
            print("Please enter path to file")
            file_path = read_line()
            with open(file_path, 'rb') as f:
                contents = f.read()
                if reciever_public_key:
                    print("=== Sending file ===")
                    response = client.deliver_message(store, reciever_public_key, contents, is_file=True, file_path=file_path)
                    if response:
                        if 'error' in response:
                            print("Error!")
                            print(response)
                        else:
                            print("Success!")
                            print(response)
                    else:
                        print("Some unknown error occured :(")
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
                        display += f"[FILE] {message['file_path']}"
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
            print("Now enter the address you would like to return the message too")
            our_return_address = read_line()
            print("Please enter the message you would like to send")
            message = read_line()
            response = client.deliver_first_message(store, host, reciever_public_key, our_return_address, message)
            if response:
                if 'error' in response:
                    print("Error!")
                    print(response)
                else:
                    print("Success!")
                    print(response)
            else:
                print("Some unknown error occured :(")
        else:
            print("You entered an incorrect option :(")
            print(help_message)
            
if __name__=="__main__":
    main()
