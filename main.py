# for getting the whatsapp qr code image
import base64

# all the web things
import selenium
from splinter import Browser
from selenium import webdriver

# for better navigation - ideally needs to be removed cos css selectors
from bs4 import BeautifulSoup

# modules used with the various bots
import time
import random
import spotipy
import spotipy.util as util
from nltk.corpus import wordnet as wn

token = util.prompt_for_user_token("YOUR EMAIL", "user-library-read")

# populate this list with the names of all chats which bots can be active on
CHATS = []
# populate this list with bots
BOTS = []
# message to add to the end of each bot message 
FOOTER = "_BEEP robot gang BOOP_"

# needed (for me at least) so that chromedriver runs headless, and so that whatsapp doesn't give out old chrome errors (don't ask me)
opts = webdriver.ChromeOptions()
opts.add_argument("user-agent=User-Agent: (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
opts.add_argument('headless')


class Whatsapp:
    
    def __init__(self, filename="qr"):
        self.browser = Browser('chrome', chrome_options=opts)
        self.browser.visit("https://web.whatsapp.com/")
        self.history = {}
        self.start_times = {}
        print("Whatsapp loaded.")

        image_div = self.find("_2EZ_m")[0]
        image = image_div.find_by_tag("img")[0]
        data = bytes(image["src"][22:], "utf8")

        with open("{}.png".format(filename), "wb") as f:
            f.write(base64.decodebytes(data))

        print("QR Code Ready")
        
        while True:
            try:
                image_div = self.find("_2EZ_m")
                if image_div == []:
                    print("Scanned")
                    break
            except selenium.common.exceptions.StaleElementReferenceException:
                print("Scanned")
                break

        while True:
            self.search = self.browser.find_by_xpath('//*[@id="side"]/div[1]/div/label/input')
            if self.search != []:
                self.search = self.search[0]
                print("Send Screen")
                break
    
    def find(self, value, tag="div", attribute="class"):
        return self.browser.find_by_css("{}[{}={}]".format(tag, attribute, value))

    def select_recipient(self, name):
        while True:
            try:
                chats = self.find("_1wjpf", tag="span")
                for c in chats:
                    if c["dir"] == "auto":
                        if c.text == name:
                            c.click()
                            return
                break
            except selenium.common.exceptions.StaleElementReferenceException:
                pass

        self.search.fill(name+"\n")
        while True:
            box = self.browser.find_by_xpath("/html/body/div/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]")
            if box != []:
                break
    
    def send_message_to(self, chat, text):
        self.select_recipient(chat)
        self.message_box = self.browser.find_by_xpath("/html/body/div/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]")[0]
        self.message_box.fill(text + "\n" + FOOTER + "\n")

    def get_current_messages(self):        
        soup = BeautifulSoup(self.browser.html)
        root = soup.find_all(name="div", attrs={"class":"_9tCEa"})[0]
        messages = []
        for message_div in root.children:
            if message_div["class"] != ["vW7d1", "_3rjxZ"]:
                message = {}
                text_divs = message_div.find_all(name="span", attrs={"class":"selectable-text"})
                if len(text_divs) == 0:
                    continue
                else:
                    text_div = text_divs[0]
                message["text"] = text_div.text
                message_div.find()
                info_div = message_div.find(attrs={"data-pre-plain-text":True})
                message["info"] = info_div["data-pre-plain-text"]
                message["24htime"] = message["info"][1:6]
                message["hour"] = int(message["24htime"].split(":")[0])
                message["minute"] = int(message["24htime"].split(":")[1])
                message["date"] = message["info"].split(",")[1].split("]")[0][1:]
                message["day"] = int(message["date"].split("/")[1])
                message["month"] = int(message["date"].split("/")[0])
                message["year"] = int(message["date"].split("/")[2])
                message["sender"] = message["info"].split("]")[-1][1:-2]
                messages.append(message)
        return messages
    
    def get_messages(self, name):
        self.select_recipient(name)
        return self.get_current_messages()
    
    def get_new_messages(self, name):
        self.select_recipient(name)
        if name not in self.history.keys():
            messages = self.get_current_messages()
            self.history[name] = messages
            smallest = 999999999
            for message in messages:
                seconds = (message["day"]*24*60) + (message["hour"]*60) + message["minute"]
                if seconds < smallest:
                    smallest = seconds
            self.start_times[name] = smallest
            return []
        
        old_messages = self.get_current_messages()
        new_messages = []
        for message in old_messages:
            if message not in self.history[name]:
                seconds = (message["day"]*24*60) + (message["hour"]*60) + message["minute"]
                if seconds > self.start_times[name]:
                    print("NEW MESSAGE", message)
                    new_messages.append(message)
        self.history[name].extend(new_messages)

        return new_messages



class DiceBot:
    def __init__(self, active_on):
        self.active_on = active_on
        self.my_messages = []
        self.name = "Dice Bot"
        self.commands_help = {"roll":"Usage: '!roll d20', rolls a 20 sided dice. Replace the number with any positive integer."}

    def filter(self, chat, messages):
        for message in messages:
            if "!roll" == message["text"][:5]:
                invalid = False
                if len(message["text"]) == 5:
                    invalid = True
                    
                else:
                    rest = message["text"][6:]
                    if rest[0] != "d":
                        invalid = True
                    try:
                        sides = int(rest[1:])
                    except ValueError:
                        invalid = True
                    if sides < 0:
                        invalid = True
                
                if invalid:
                    text = "Oops! That's not right. Try !help roll"
                    app.send_message_to(chat, text)
                    self.my_messages.append(text)
                    
                else:
                    num = random.randint(0, sides)
                    text = "{} rolled a {} on the {}!".format(message["sender"], num, rest)
                    self.my_messages.append(text)
                    app.send_message_to(chat, text)
                        

        

class HelpBot:
    def __init__(self, active_on):
        self.active_on = active_on
        self.my_messages = []
        self.name = "Help Bot"
        self.commands_help = {"help":"!help will give a list of all available commands, and !help (COMMAND NAME) will give information about the usuage of a particular command. Thank you!", "aboutme":"!aboutme will give some helpful information about this bot system."}

    def filter(self, chat, messages):
        commands = {}
        for bot in BOTS:
            commands.update(bot.commands_help)
        for message in messages:
            if message["text"] == "!help":
                stub = "Here are all the available commands:\n"
                for c in commands.keys():
                    stub += c + "\n"
                self.my_messages.append(stub)
                app.send_message_to(chat, stub)
            elif message["text"][:5] == "!help":
                rest = message["text"][6:]
                if rest in commands.keys() or "!" + rest in commands.keys():
                    text = commands[rest]
                    self.my_messages.append(text)
                    app.send_message_to(chat, text)
                else:
                    text = "Sorry, that's not one of the listed commands."
                    self.my_messages.append(text)
                    app.send_message_to(chat, text)
            elif message["text"] == "!aboutme":
                text = "Hi there! I'm a bot. I've got a bunch of useful commands! You can find a list of them using !help or !help (COMMAND NAME) to find out about specific commands. Happy to be of service!" 
                self.my_messages.append(text)
                app.send_message_to(chat, text)
        

class ReminderBot:
    def __init__(self, active_on):
        self.active_on = active_on
        self.my_messages = []
        self.name = "Reminder Bot"
        self.commands_help = {"remindme":"Usage: '!remindme 2 minutes', sends a reminder in two minutes. Replace the number with any positive integer. And the 'days' with any normal measure of time."}
        self.timers = []

    def filter(self, chat, messages):
        for message in messages:
            if message["text"][:9].lower() == "!remindme":
                try:
                    parts = message["text"].split(" ")
                    num = float(parts[1])
                    measure = parts[2]
                    intervals = {"day":86400, "days":86400, "min":60, "mins":60, "minute":60, "minutes":60, "s":1, "second":1, "seconds":1, "hour":3600, "h":3600, "hours":3600, "year":31557600, "years":31557600}
                    if measure not in intervals.keys():
                        raise Exception
                    seconds = intervals[measure] * num
                    self.timers.append((time.time() + seconds, message["sender"], time.strftime("%d/%m/%y, %H:%M:%S", time.localtime())))
                    text = "I'll remind you on {}".format(time.strftime("%d/%m/%y, %H:%M:%S", time.localtime(time.time()+seconds)))
                    self.my_messages.append(text)
                    app.send_message_to(chat, text)
                except Exception as e:
                    print(e, e.__traceback__)
                    text = "Oops! That's not right. Try !help remindme"
                    self.my_messages.append(text)
                    app.send_message_to(chat, text)
        
        for timer in self.timers:
            if time.time() > timer[0]:
                text = "Reminder for {} from {}!".format(timer[1], timer[2])
                self.my_messages.append(text)
                app.send_message_to(chat, text)
                self.timers.remove(timer)


class MediaBot:
    def __init__(self, active_on):
        self.active_on = active_on
        self.my_messages = []
        self.name = "Media Bot"
        self.commands_help = {"youtube":"Usage: '!youtube pewdiepie', searches youtube for pewdiepie. Replace the second word with your search query.", "yt":"!yt pewdiepie', searches youtube for pewdiepie. Replace the second word with your search query.", "spotify":"!spotify adele', searches spotify for adele. Replace the second word with your search query."}
        self.youtube_url = "https://www.youtube.com/results?search_query="
        self.spotify_url = "https://open.spotify.com/search/results/"
        self.sp = spotipy.Spotify(auth=token)

    def yt_cmd(self, chat, message):
        parts = message["text"].split(" ")
        if len(parts) == 1:
            text = "Oops! That's not right. Try !help youtube"
            self.my_messages.append(text)
            app.send_message_to(chat, text)
        else:
            url = self.youtube_url + "+".join(parts[1:])
            self.my_messages.append(url)
            app.send_message_to(chat, url)

    def filter(self, chat, messages):
        for message in messages:
            if message["text"][:8] == "!youtube":
                self.yt_cmd(chat, message)
            elif message["text"][:3] == "!yt":
                self.yt_cmd(chat, message)
            elif message["text"][:8] == "!spotify":
                parts = message["text"].split(" ")
                if len(parts) == 1:
                    text = "Oops! That's not right. Try !help spotify"
                    self.my_messages.append(text)
                    app.send_message_to(chat, text)
                else:
                    print(" ".join(parts[1:]))
                    resp = self.sp.search(q=" ".join(parts[1:]))
                    if len(resp["tracks"]["items"]) == 0:
                        text = "Sorry, I couldn't find anything for that."
                        self.my_messages.append(text)
                        app.send_message_to(chat, text)
                    else:
                        url = resp["tracks"]["items"][0]["external_urls"]["spotify"]
                        self.my_messages.append(url)
                        app.send_message_to(chat, url)


class TextBot:
    def __init__(self, active_on):
        self.active_on = active_on
        self.my_messages = []
        self.name = "Text Bot"
        self.commands_help = {"spongebob":"Usage: '!spongebob hello', will send a message with 'hello' randomly capitalised.", "thesaurize":"Usuage !thesaurize hello what's up. Will swap every word with a synonym."}

    def filter(self, chat, messages):
        for message in messages:
            if message["text"][:10].lower() == "!spongebob":
                parts = message["text"].split(" ")
                if len(parts) == 1:
                    text = "Oops! That's not right. Try !help spongebob"
                    self.my_messages.append(text)
                    app.send_message_to(chat, text)
                else:
                    spongebobed = ""
                    n = 0
                    for c in " ".join(parts[1:]):
                        n += 1
                        if n%2:
                            spongebobed += c.upper()
                        else:
                            spongebobed += c.lower()

                    self.my_messages.append(spongebobed)
                    app.send_message_to(chat, spongebobed)
            if message["text"][:11].lower() == "!thesaurize":
                parts = message["text"].split(" ")
                if len(parts) == 1:
                    text = "Oops! That's not right. Try !help thesaurize"
                    self.my_messages.append(text)
                    app.send_message_to(chat, text)
                else:
                    new = ""
                    for word in parts[1:]:
                        synonyms = wn.synsets(word)
                        if len(synonyms) == 0:
                            synonym = word
                        else:
                            synset = random.choice(synonyms)
                            synonym = random.choice(synset.lemmas()).name()
                        
                        new += synonym + " "
                    self.my_messages.append(new)
                    app.send_message_to(chat, new)



BOTS += [DiceBot(['''Add active chats for this bot here''']), HelpBot([]), ReminderBot([]), MediaBot([]), TextBot([])]

app = Whatsapp()

while True:
    for chat in CHATS:
        messages = app.get_new_messages(chat)
        if len(messages) != 0:
            print(messages)
        
        for bot in BOTS:
            if chat in bot.active_on:
                try:
                    for n, newmessage in enumerate(messages):
                        for oldmessage in bot.my_messages:
                            if oldmessage == newmessage["text"]:
                                try:
                                    messages.pop(n)
                                except IndexError as e:
                                    print(e, e.__traceback__)

                    bot.filter(chat, messages)
                except Exception as e:
                    text = "{} encountered an error while dealing with those messages. ERROR:\n\n{}\n{}".format(bot.name,e.__traceback__, e)

