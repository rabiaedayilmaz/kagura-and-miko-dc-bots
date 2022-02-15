import random
import asyncio
import discord
from keep_alive import keep_alive

cli = discord.Client

# channel ids
study_session_channel_id = "enter here channel id as int"
to_do_list_channel_id = "enter here channel id as int"

# user ids
_user1 = "enter here user1 id as int"
_user2 = "enter here user2 id as int"

with open("token.txt", "r") as f:
  _TOKEN = f.read()


class kaguraClient(cli):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.study_start = False
        self.session = 90000    # equals 25 min
        self._user1_session = 0
        self._user2_session = 0
        self.motivation_emojis = [
                                  "\U0001F525", "\U00012728", "\U0001F98B",
                                  "\U0001F308", "\U0001F49B", "\U0001F5A4",
                                  "\U0001F49C", "\U0001F4AA", "\U00012714",
                                  "\U0001F47E", "\U0001F4AF", "\U0001F91F",
                                  "\U00002622",
                                  ]
        self._user1 = _user1
        self._user2 = _user2

    async def on_ready(self):
        print(f"Logged as: {self.user}, ID: {self.user.id}")

    async def on_message(self, message):
        # bot shouldn't reply itself
        if message.author.id == self.user.id:
            return

        if message.content == "-whoami":
            await message.reply("To define is to limit.")
        elif message.content == "-whoareyou":
            await message.reply("Reflection on the mirror.")
        # wave hand to any stranger who greets
        elif message.content.lower().startswith("hello") or message.content.lower().startswith("hi"):
            await message.add_reaction("\U0001F44B")
        # motivate with emojis when writing to to-do-list channel
        if message.channel.id == to_do_list_channel_id:
            if any([i.isdigit() for i in message.content]):
                await message.add_reaction(random.choice(self.motivation_emojis))

        # study-session counter
        if message.channel.id == study_session_channel_id:
            # start session
            if ".study" in message.content:
                self.study_start = True
                await message.channel.send("GET READY TO STUDY!")
                await asyncio.sleep(1)
                await message.channel.send("3")
                await asyncio.sleep(1)
                await message.channel.send("2")
                await asyncio.sleep(1)
                await message.channel.send("1")
                await asyncio.sleep(1)
                await message.channel.send(f"SESSION STARTED, GOOD LUCK!! {message.author.mention}")

                while self.study_start:
                    if self.session == 18000:
                        await message.channel.send("5 min. is left.")
                    elif self.session == 3600:
                        await message.channel.send("1 min. is left.")
                    elif self.session == 0:
                        await message.channel.send("TIME IS OUT!! WELL DONE :)")
                        if message.author.id == _user1:
                            self._user1_session += 1
                            with open("session_counter.txt", "a") as f:
                                f.write(f"Sessions' {message.author}: {self._user1_session}")
                        if message.author.id == _user2:
                            self._user2_session += 1
                            with open("session_counter.txt", "a") as f:
                                f.write(f"Sessions' {message.author}: {self._user2_session}")
                        break
                    else:
                        self.session -= 1
                        await asyncio.sleep(1)

            if message.content == ".count":
                await message.channel.send("Counted Sessions:\n")
                with open("session_counter.txt", "r") as f:
                    if f.read() == "":
                        await message.channel.send("Umm... No record :D")
                    else:
                        await message.channel.send(f)


client = kaguraClient()
keep_alive()
client.run(_TOKEN)
