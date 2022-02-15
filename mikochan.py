import asyncio
from keep_alive import keep_alive
import discord  # api
import random   # for random selection
import requests
import os
import json

client = discord.Client     # client

# messages to motivate users if they write to-do-list before midnight
mid_msg_list = ["Isn't it nice to think that tomorrow is a new day with no mistakes in it yet?",
                "The next morning dawned bright and sweet, like ribbon candy.",
                "Today is the first day of the rest of your life.",
                "Daily dance uplift the soul to spiritual realms.",
                "Another day, another chance.",
                "Yesterday is history, tomorrow is a mystery, today is a gift of God, which is why we call it the present.",
                "You cannot swim for new horizons until you have courage to lose sight of the shore.",
                "You can cut all the flowers but you cannot keep Spring from coming.",
                "Don't be pushed around by the fears in your mind. Be led by the dreams in your heart.",
                "Lack of direction, not lack of time, is the problem. We all have twenty-four hour days.",
                "The man who moves a mountain begins by carrying away small stones.",
                "If you believe very strongly in something, stand up and fight for it.",
                "Life is short. Focus on what really matters most. You have to change your priorities over time.",
                "Never a failure,always a lesson.",
                "Be yourself; everyone else is already taken.",
                "You've gotta dance like there's nobody watching,\n"
                "Love like you'll never be hurt,\n"
                "Sing like there's nobody listening,\n"
                "And live like it's heaven on earth.",
                "We are all in the gutter, but some of us are looking at the stars.",
                "Fairy tales are more than true: not because they tell us that dragons exist, but because they tell us that dragons can be beaten.",
                "Everything you can imagine is real.",
                "Life isn't about finding yourself. Life is about creating yourself.",
                "Listedeki sürpriz cümleye denk geldin: o zaman yarın, harika günlerden biri olmalı!"
                "Do what you feel in your heart to be right – for you’ll be criticized anyway.",
                "Peace begins with a smile :)",
                "Pain is inevitable. Suffering is optional.",
                "It isn't what you have or who you are or where you are or what you are doing that makes you happy or unhappy. It is what you think about it.",
                "Don't judge each day by the harvest you reap but by the seeds that you plant.",
                "Clouds come floating into my life, no longer to carry rain or usher storm, but to add color to my sunset sky.",
                "It is the time you have wasted for your rose that makes your rose so important.",
                "You were born with wings, why prefer to crawl through life?",
                "Do one thing every day that scares you.",
                "The unexamined life is not worth living."]

# emoji list
motivation_emojis = [
                     "\U0001F525", "\U00012728", "\U0001F98B",
                     "\U0001F308", "\U0001F49B", "\U0001F5A4",
                     "\U0001F49C", "\U0001F4AA", "\U00012714",
                     "\U0001F64C", "\U0001F4AA", "\U0001F955",
                     "\U0001F966", "\U0001F355", "\U0001F436",
                     "\U000026A1", "\U0001F3AF", "\U0001F90D",
                     ]

# channel list
to_do_list_channel_id = "enter channel id as int"

# user ids
_user1 = "enter user1 id as int"
_user2 = "enter user2 id as int"

max_lines = 10   # max limit lines
pomi_user_1, pomi_user_2 = 0, 0   # pomi points for every daily attempt to to_do_list_channel

# time api url
TIME_API_URL =  "http://worldtimeapi.org/api/timezone/Europe/Istanbul"

# help messages
remind_help_msg = "Hi! I'm Miko: your reminder and task tracker :)\n" \
                  "\nMax. task: 10\nMax interval for timer: 30 m\n" \
                  "\n!Only hours (h) and minutes (m) are allowed!\n" \
                  "\nUsage of Reminder List:\t<reminder message> + <reminder time span>" \
                  "\nExample:\tDrink magical tea + 1h 10m" \
                  "\nUsage of Task List:\t<task message>++" \
                  "\nExample:\tRead black spellbook++\n" \
                  "\nTo start timer: .time mm\n" \
                  "\nTo view pomi-points list:\t.pomi" \
                  "\nTo clear all:\t.clear all" \
                  "\nTo clear task list:\t.clear t" \
                  "\nTo clear reminder list:\t.clear r" \
                  "\nTo list tasks:\t.list t" \
                  "\nTo list reminders:\t.list r"


# some functions
def clear_task_list(task_list):
    with open(task_list, "w") as r:
        r.write("")


def clear_reminder_list(rem_list):
    with open(rem_list, "w") as r:
        r.write("")

def time_converter(user_time):
    if len(user_time.split()) == 2:     # check if it has 2 arg format: timer + min
        m = user_time.split()[1]
        minute = (m.split("m")[0])
        min_in_sec = int(minute) * 60
        return min_in_sec

    else:   # check if it has 1 arg : i.e. reminder
        minute = user_time.split("m")[0]
        min_in_sec = int(minute) * 60
        return min_in_sec


def get_current_time_api():
    response = requests.get(TIME_API_URL)
    data = response.text
    parse_json = json.loads(data)

    active_case = parse_json["datetime"]
    t = active_case[11:19]
    h, m, s = t[0:2], t[3:5], t[6::]    # hours, mins, secs
    return h, m, s


def midnight_dm():
    # dm motivate
    letsgo = False
    h, m, s = get_current_time_api()
    if int(h) == 23 or int(h) == 0:
        letsgo = True
    return letsgo, random.choice(mid_msg_list)

def reminder(remind_hour, remind_min):
    h, m, _ = get_current_time_api()
    if int(h) == int(remind_hour) and int(m) == int(remind_min):
        return True
    return False

def reminder_msg():
    return f"Hey, do not forget to complete!\n!"

class MikoBot(client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.motivation_emojis = motivation_emojis
        self.timer_start = False
        self.remindme = False
        self.remindertime = ""
        self.count_for_spam = 0
        self._user1, self._user2 = _user1, _user2
        self.pomi_user_1, self.pomi_user_2 = pomi_user_1, pomi_user_2
        if midnight_dm() != None:
            self.letsgo, self.mi = midnight_dm()


    async def on_ready(self):
        print(f"Logged as: {self.user}, ID: {self.user.id}")


    async def on_message(self, message):
        # do not reply self
        if message.author.id == self.user.id:
            return
        while self.letsgo:
            dm_msg = "---\nJust finished another day, congrats!Here's a quote:\n" + self.mi + "\n---"
            if self.count_for_spam == 0:
                user1 = await client.fetch_user(self._user1)
                await user1.send(dm_msg)
                user2 = await client.fetch_user(self._user2)
                await user2.send(dm_msg)
                self.count_for_spam = 1
                break

        # remind help menu
        if message.content == ".help":
            await message.reply(remind_help_msg)
        
        # logs for user1
        if message.author.id == self._user1:
            rem_list = "reminder_list_1.txt"
            task_list = "task_list_1.txt"
        # logs for user2
        if message.author.id == self._user2:
            rem_list = "reminder_list_2.txt"
            task_list = "task_list_2.txt"


        if message.content == ".clear all":
            clear_reminder_list(rem_list)
            clear_task_list(task_list)
            await message.reply(f"All lists are successfully cleared for {message.author.mention}.")
        elif message.content == ".clear r":
            clear_reminder_list(rem_list)
            await message.reply("Reminder list is successfully cleared.")
        elif message.content == ".clear t":
            clear_task_list(task_list)
            await message.reply("Task list is successfully cleared.")
        elif message.content == ".list t":
            if os.stat(task_list).st_size==0:
                await message.channel.send("List is empty.")
            with open(task_list, "r") as l:
                li = "".join([">>" + str(i) for i in l])
                await message.channel.send(li)
        elif message.content == ".list r":
            if os.stat(rem_list).st_size==0:
                await message.channel.send("List is empty.")
            else:
                with open(rem_list, "r") as l:
                    li = "".join([">> Remind: " + str(i.split()[0] + "\tTime: " + str(i.split()[1] + "\tAttained to: " + str(i.split()[-1]))) for i in l])
                    await message.channel.send(li)
        elif "++" in message.content:
            current_line = sum(1 for i in open(task_list))
            if current_line >= max_lines:
                await message.channel.send("List is full!\nComplete your tasks or clear and try again.")
            task_name = message.content.split("++")[0]
            with open(task_list, "a") as a:
                a.write(f"{task_name} --> {message.author}\n")
            msg1 = f'You have this task: \"{task_name}\",'
            msg2 = "Good luck!!"
            breaker_msg = (len(msg1) + len(msg2)) * "-"
            await message.author.send(breaker_msg + "\n\t" + msg1 + "\n\t" + msg2 + "\n" + breaker_msg)

        elif "+" in message.content:
            if not any(i.isdigit() for i in message.content):
                await message.channel.send("T-there is no number to measure time...")
            else:
                if "http" in message.content:     # ignore urls
                    return

                current_line = sum(1 for i in open(rem_list))
                if current_line >= 2:
                    await message.channel.send("You can set one reminder!!")
                reminder_name, reminder_time = message.content.split("+")
                with open(rem_list, "a") as a:
                    a.write(f"{reminder_name} {reminder_time} {message.author}\n")
                msg_r = f"I will remind you \"{reminder_name}\" {reminder_time} later!!"
                await message.author.send(msg_r)

                rem_sec = time_converter(reminder_time)
                while rem_sec > 0:
                    await asyncio.sleep(1)
                    rem_sec -= 1
                await message.author.send("Psst... do you remember your top secret task?")

        elif message.content == ".pomi":
            with open("pomi_points.txt", "r") as f:
                pomi = "".join([">>"+line for line in f])
                await message.channel.send(pomi)

        if message.content == "good girl":
            await message.channel.send("Yes, i am :3")

        # to do list channel
        if message.channel.id == to_do_list_channel_id:
            # send random emojis
            if any([i.isdigit() for i in message.content]):
                if not message.content.startswith(".time"):
                    await message.add_reaction(random.choice(self.motivation_emojis))
                    with open("pomi_points.txt", "w") as f:
                        if message.author.id == self._user1:
                            self.pomi_user_1 += 5
                            f.write(f"User1 pomi-points: {self.pomi_user_1}")
                        elif message.author.id == self._user2:
                            self.pomi_user_2 += 5
                            f.write(f"User2 pomi points: {self.pomi_user_2}\n")
                        else:
                            print("User error in pomi-points.")

        # timer
        if message.content.startswith(".time"):
            self.timer_start = True
            t = message.content
            total_sec = time_converter(t)

            if total_sec < 0:
                await message.channel.send("Seconds is negative, impossible! Unless you are a time traveler.")
            elif total_sec == 0:
                await message.channel.send("Time is out, lol.")
            elif total_sec > 1800:
                await message.channel.send("Max interval for timer is 30 m!!! Counting more is so boring...")
            else:
                await message.channel.send("STARTED!")
            while self.timer_start:
                total_sec -= 1
                await asyncio.sleep(1)
                if total_sec == 901:
                    await message.channel.send("15 min is left.")
                if total_sec == 301:
                    await message.channel.send("5 min. is left.")
                if total_sec == 61:
                    await message.channel.send("1 min. is left.")
                if total_sec == 15:
                    await message.channel.send("15 sec. is left.")
                if total_sec == 0:
                    await message.channel.send(f"TIME IS OUT!!{message.author.mention}")
                    break


# get the token
with open("token.txt", encoding="utf-8") as f:
    _TOKEN = f.read()

client = MikoBot()
keep_alive()    # run continuously
client.run(_TOKEN)
