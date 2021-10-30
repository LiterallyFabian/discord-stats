import os
import re
from User import User
from Message import Message

# removes timestamps and stuff from the csv entries


def get_message(line):
    return re.sub("\d{18},\d{4}-\d{2}-\d{2} .+\+00:00,", "", line).lower()


messages_path = input("Messages path (messages/): ") or "messages"
query = input("Word to count (leave blank for all messages): ").lower()
all_messages = []

for message_dir in os.listdir(messages_path):
    user = User(message_dir, message_dir)
    message = Message(user, query)

    # open message file
    if(message_dir != "index.json"):
        with open(os.path.join(messages_path, message_dir, "messages.csv"), encoding="utf8") as file:
            # Ignore first line, could be replaced with .pop or something but whatever
            first_line = True
            for unparsed_line in file:
                if not first_line:
                    line = get_message(unparsed_line.rstrip())
                    message.count += line.count(query)
                else:
                    first_line = False

            all_messages.append(message)

all_messages.sort(key=lambda x: x.count, reverse=True)
print(all_messages[0].count)
