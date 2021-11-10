import os
import re
import json
import pandas as pd
import matplotlib.pyplot as plt
from User import User
from Message import Message


def get_message(line):  # removes timestamps and stuff from the csv entries
    return re.sub("\d{18},\d{4}-\d{2}-\d{2} .+\+00:00,", "", line).lower()


def get_words(line, query):
    return len(re.findall(fr"^{query}|{query}$|{query}[^a-zA-Z]", line))


messages_path = input("Messages path (messages/): ") or "messages"

# parse the index file
index = open(os.path.join(messages_path, "index.json"))
user_data = json.load(index)


def plot_user():
    while(True):
        name_found = False

        # find an user in the user list
        while(name_found == False):
            query = input("\nUser to plot (username): ").lower()
            for id in user_data:
                if(user_data[id] is not None):
                    name = user_data[id].replace("Direct Message with ", "")
                    user = User(id, name)
                    if(user.name.lower().startswith(query)):
                        name_found = True
                        break
            if(name_found == False):
                print("User not found, please try again")

        print(f"{user.name} (ID {user.id}) found.")

        df = pd.read_csv(os.path.join(
            messages_path, f"c{user.id}", "messages.csv"), sep=",", encoding="utf8", usecols=["Timestamp"])
        df["Timestamp"] = df["Timestamp"].astype("datetime64")
        df.groupby([df["Timestamp"].dt.year, df["Timestamp"].dt.month]
                   ).count().plot(kind="bar")

        plt.xticks(rotation=45)
        plt.title(f"Messages sent to {user.name} every month")
        plt.show()


def count_word():
    while(True):
        query = input("\nWord to count: ").lower()
        all_messages = []

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
                            message.count += get_words(line, query)
                        else:
                            first_line = False

                    all_messages.append(message)

        all_messages.sort(key=lambda x: x.count, reverse=True)

        for msg in all_messages:
            if(msg.count > 0):
                print('{:10}   {:4}'.format(msg.count, msg.user.name))


# ask user if they want to plot users or count words
while(True):
    print("\nPlot users (p) or count words (c)?")
    choice = input("(p/c): ").lower()
    if(choice == "p"):
        plot_user()
    elif(choice == "c"):
        count_word()
    else:
        print("Invalid input")
