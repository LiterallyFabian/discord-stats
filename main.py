import os
import re
import json
from User import User
from Message import Message


def get_message(line):  # removes timestamps and stuff from the csv entries
    return re.sub("\d{18},\d{4}-\d{2}-\d{2} .+\+00:00,", "", line).lower()


def count_words(line, query):
    return len(re.findall(fr"^{query}|{query}$|{query}[^a-zA-Z]", line))


messages_path = input("Messages path (messages/): ") or "messages"
while(True):
    query = input("\nWord to count: ").lower()
    all_messages = []

    # parse the index file
    index = open(os.path.join(messages_path, "index.json"))
    user_data = json.load(index)

    for message_dir in os.listdir(messages_path):
        # open message file
        if(message_dir != "index.json" and message_dir[1:] in user_data):
            user = User(message_dir, user_data[message_dir[1:]])
            message = Message(user, query)
            with open(os.path.join(messages_path, message_dir, "messages.csv"), encoding="utf8") as file:
                # Ignore first line, could be replaced with .pop or something but whatever
                first_line = True
                for unparsed_line in file:
                    if not first_line:
                        line = get_message(unparsed_line.rstrip())
                        message.count += count_words(line, query)
                    else:
                        first_line = False

                all_messages.append(message)

    all_messages.sort(key=lambda x: x.count, reverse=True)

    for msg in all_messages:
        if(msg.count > 0):
            print('{:10}   {:4}'.format(msg.count, msg.user.name))
