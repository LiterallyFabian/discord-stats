import os
from User import User
from Message import Message

messages_path = input("Messages path (messages/): ") or "messages"
query = input("Word to count (leave blank for all messages): ")


for message_dir in os.listdir(messages_path):
    user = User(19, "h")
    message = Message(user, query)

    # open message file
    with open(os.path.join(messages_path, message_dir, "messages.csv")) as file:
        for line in file:
            print(line.rstrip())

    break
